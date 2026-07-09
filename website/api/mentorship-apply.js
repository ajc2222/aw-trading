// POST /api/mentorship-apply
// Validates a mentorship application, emails the review team and applicant via Resend.

const MAX_LEN = { name: 100, email: 254, discord: 64, experience: 40, why: 1500 };

// ---------------------------------------------------------------------------
// In-memory IP rate limiter — 3 submissions per IP per 10-minute window.
// The Map persists across warm serverless invocations within the same instance.
// NOTE: This is per-instance only. Under concurrent cold starts an attacker
// could submit more than 3 times. A production upgrade would use Vercel KV
// or Upstash Redis for distributed rate state.
// ---------------------------------------------------------------------------
const RATE_LIMIT_MAX = 3;
const RATE_LIMIT_WINDOW_MS = 10 * 60 * 1000; // 10 minutes

/** @type {Map<string, number[]>} ip → sorted array of submission timestamps */
const ipTimestamps = new Map();

function isRateLimited(ip) {
  const now = Date.now();
  const windowStart = now - RATE_LIMIT_WINDOW_MS;

  // Cap map size to prevent memory exhaustion under heavy load.
  if (ipTimestamps.size > 10_000) {
    const entries = [...ipTimestamps.entries()];
    entries.sort((a, b) => a[1][a[1].length - 1] - b[1][b[1].length - 1]);
    for (const key of entries.slice(0, entries.length - 10_000).map(([k]) => k)) {
      ipTimestamps.delete(key);
    }
  }

  // Purge entries whose entire timestamp list has expired to prevent unbounded growth.
  for (const [key, timestamps] of ipTimestamps) {
    const fresh = timestamps.filter((t) => t > windowStart);
    if (fresh.length === 0) {
      ipTimestamps.delete(key);
    } else {
      ipTimestamps.set(key, fresh);
    }
  }

  const timestamps = ipTimestamps.get(ip) || [];
  const recent = timestamps.filter((t) => t > windowStart);

  if (recent.length >= RATE_LIMIT_MAX) {
    return true;
  }

  recent.push(now);
  ipTimestamps.set(ip, recent);
  return false;
}

function clean(value, max) {
  if (typeof value !== 'string') return '';
  return value.trim().slice(0, max);
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

async function notifyReviewers(app) {
  const apiKey = process.env.RESEND_API_KEY;
  const fromEmail = process.env.MENTORSHIP_FROM_EMAIL;
  if (!apiKey || !fromEmail) return { sent: false, reason: 'email-not-configured' };

  const recipients = (process.env.MENTORSHIP_NOTIFY_EMAILS || '')
    .split(',')
    .map((e) => e.trim())
    .filter(Boolean);
  if (!recipients.length) return { sent: false, reason: 'no-recipients-configured' };

  const results = await Promise.all(
    recipients.map(async (email) => {
      try {
        const body = `New mentorship application\n\nName: ${app.name}\nEmail: ${app.email}\nDiscord: ${app.discord}\nExperience: ${app.experience}\nWhy: ${app.why}\nSubmitted: ${new Date(app.submittedAt).toISOString()}`;
        const res = await fetch('https://api.resend.com/emails', {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${apiKey}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            from: fromEmail,
            to: email,
            subject: 'New Mentorship Application',
            text: body,
          }),
        });
        return { email, sent: res.ok, status: res.status };
      } catch (err) {
        return { email, sent: false, error: String(err) };
      }
    })
  );

  return { sent: results.some((r) => r.sent), results };
}

async function sendConfirmationEmail(app) {
  const apiKey = process.env.RESEND_API_KEY;
  const fromEmail = process.env.MENTORSHIP_FROM_EMAIL;
  if (!apiKey || !fromEmail) return;

  await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from: fromEmail,
      to: app.email,
      subject: 'AW Trading — Application received',
      text: `Hey ${app.name || 'there'},\n\nYour mentorship application has been received. AW reviews every application personally — you'll hear back within a few days.\n\n— AW Trading`,
    }),
  });
}

export default async function handler(req, res) {
  // CORS headers: set before any early return so preflight OPTIONS sees them.
  res.setHeader('Access-Control-Allow-Origin', 'https://awtrading.com');
  res.setHeader('Access-Control-Allow-Methods', 'POST');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // Handle CORS preflight.
  if (req.method === 'OPTIONS') {
    return res.status(204).end();
  }

  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ ok: false, error: 'method_not_allowed' });
  }

  // Origin/Referer sanity check to mitigate cross-origin abuse.
  const origin = req.headers.origin || req.headers.referer || '';
  if (origin && !origin.startsWith('https://awtrading.com')) {
    return res.status(403).json({ ok: false, error: 'forbidden' });
  }

  let body = req.body;
  if (typeof body === 'string') {
    try {
      body = JSON.parse(body);
    } catch {
      return res.status(400).json({ ok: false, error: 'invalid_json' });
    }
  }
  if (!body || typeof body !== 'object') {
    return res.status(400).json({ ok: false, error: 'invalid_body' });
  }

  // Rate limit: fail fast before any further processing or email calls.
  // Vercel sets x-forwarded-for reliably; the first entry is the client IP.
  const forwardedFor = req.headers['x-forwarded-for'];
  const ip = (typeof forwardedFor === 'string'
    ? forwardedFor.split(',')[0].trim()
    : req.socket?.remoteAddress) || 'unknown';
  if (isRateLimited(ip)) {
    return res.status(429).json({ ok: false, error: 'rate_limited' });
  }

  // Honeypot: bots fill every field, humans never see or fill this one.
  if (clean(body.company, 100)) {
    return res.status(200).json({ ok: true });
  }

  const application = {
    name: clean(body.name, MAX_LEN.name),
    email: clean(body.email, MAX_LEN.email),
    discord: clean(body.discord, MAX_LEN.discord),
    experience: clean(body.experience, MAX_LEN.experience),
    why: clean(body.why, MAX_LEN.why),
    submittedAt: Date.now(),
  };

  if (!application.name || !application.email) {
    return res.status(400).json({ ok: false, error: 'missing_required_fields' });
  }
  if (!isValidEmail(application.email)) {
    return res.status(400).json({ ok: false, error: 'invalid_email' });
  }

  try {
    await Promise.all([
      notifyReviewers(application).catch(() => {}),
      sendConfirmationEmail(application).catch(() => {}),
    ]);

    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('mentorship-apply error', err);
    return res.status(500).json({ ok: false, error: 'internal_error' });
  }
}
