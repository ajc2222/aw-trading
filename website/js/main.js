/* =========================================================
   AW TRADING — SHARED JS
   Every feature below no-ops if its elements aren't on the page.
   ========================================================= */

/* =========================================================
   CONFIG — paste real values here before launch.
   ========================================================= */

// --- Stripe Payment Links -----------------------------------------------
// Replace each placeholder with the real Stripe Payment Link URL.
// Any button whose href still starts with "#stripe-todo" gets a
// data-todo="stripe" flag and a console.warn in dev so it can't ship silently.
const STRIPE_LINKS = {
  foundations: 'https://whop.com/aw-trading-discord',   // index: $49/mo Foundations
  liveTrader: 'https://whop.com/aw-trading-discord',    // index: $129/mo Live Trader
  innerCircle: 'https://whop.com/aw-trading-discord',   // index: $499/mo Inner Circle (Apply)
  indicatorOnly: 'https://whop.com/aw-trading-discord', // indicator: $39/mo Indicator Only
  indicatorBundle: 'https://whop.com/aw-trading-discord' // indicator: bundled Live Trader CTA
};

// --- Giveaway countdown ---------------------------------------------------
// LOUD REMINDER: update this before every giveaway cycle. Format: local time.
const GIVEAWAY_END = new Date('2026-07-31T20:00:00');

/* ========================================================= */

(function () {
  'use strict';

  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- scroll reveals ---------- */
  (function reveals() {
    const els = document.querySelectorAll('.reveal');
    if (!els.length) return;
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          e.target.classList.add('in');
          io.unobserve(e.target);
        }
      });
    }, { threshold: .15 });
    els.forEach((el) => io.observe(el));
  })();

  /* ---------- count-up stats ---------- */
  (function countUp() {
    const els = document.querySelectorAll('[data-count]');
    if (!els.length) return;
    const cio = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        const el = e.target, target = +el.dataset.count, n = el.querySelector('.n');
        if (!n) { cio.unobserve(el); return; }
        if (reducedMotion) { n.textContent = target; cio.unobserve(el); return; }
        n.style.color = '#2E6BFF';
        n.style.transition = 'color .5s';
        const t0 = performance.now(), dur = 1400;
        (function tick(t) {
          const p = Math.min((t - t0) / dur, 1), ease = 1 - Math.pow(1 - p, 3);
          n.textContent = Math.round(target * ease);
          if (p < 1) requestAnimationFrame(tick); else n.style.color = '';
        })(t0);
        cio.unobserve(el);
      });
    }, { threshold: .5 });
    els.forEach((el) => cio.observe(el));
  })();

  /* ---------- mobile nav (compact sheet) ---------- */
  (function mobileNav() {
    const burger = document.querySelector('.nav-burger');
    const overlay = document.querySelector('.mobile-nav');
    const backdrop = document.querySelector('.mobile-nav-backdrop');
    if (!burger || !overlay) return;

    function syncTop() {
      const nav = document.querySelector('nav');
      if (!nav) return;
      const t = nav.getBoundingClientRect().bottom + 'px';
      overlay.style.top = t;
      if (backdrop) backdrop.style.top = t;
    }

    function openNav() {
      syncTop();
      overlay.classList.add('open');
      if (backdrop) backdrop.classList.add('open');
      burger.setAttribute('aria-expanded', 'true');
      burger.setAttribute('aria-label', 'Close navigation');
      document.addEventListener('keydown', onKeydown);
    }

    function closeNav() {
      overlay.classList.remove('open');
      if (backdrop) backdrop.classList.remove('open');
      burger.setAttribute('aria-expanded', 'false');
      burger.setAttribute('aria-label', 'Open navigation');
      document.removeEventListener('keydown', onKeydown);
    }

    function onKeydown(e) {
      if (e.key === 'Escape') closeNav();
    }

    burger.addEventListener('click', () => {
      overlay.classList.contains('open') ? closeNav() : openNav();
    });
    if (backdrop) backdrop.addEventListener('click', closeNav);
    overlay.querySelectorAll('.mobile-nav-links a').forEach((a) => {
      a.addEventListener('click', closeNav);
    });
    window.addEventListener('scroll', () => {
      if (overlay.classList.contains('open')) syncTop();
    }, { passive: true });
  })();

  /* ---------- Stripe CTA wiring ---------- */
  (function stripeLinks() {
    const btns = document.querySelectorAll('[data-stripe]');
    if (!btns.length) return;
    btns.forEach((btn) => {
      const key = btn.getAttribute('data-stripe');
      const url = STRIPE_LINKS[key];
      if (!url) return;
      btn.setAttribute('href', url);
      if (url.startsWith('#stripe-todo')) {
        btn.setAttribute('data-todo', 'stripe');
        console.warn(`[AW Trading] Stripe Payment Link not set for "${key}". Update STRIPE_LINKS in js/main.js.`);
      }
    });
  })();

  /* ---------- copy-code buttons (prop-firms) ---------- */
  (function copyCode() {
    const btns = document.querySelectorAll('.copy');
    if (!btns.length) return;

    function fallbackCopy(text) {
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.focus();
      ta.select();
      try { document.execCommand('copy'); } catch (e) { /* no-op */ }
      document.body.removeChild(ta);
    }

    function withTimeout(promise, ms) {
      return Promise.race([
        promise,
        new Promise((_, reject) => setTimeout(() => reject(new Error('clipboard timeout')), ms))
      ]);
    }

    btns.forEach((b) => b.addEventListener('click', async () => {
      const code = b.dataset.code;
      if (navigator.clipboard && window.isSecureContext) {
        try { await withTimeout(navigator.clipboard.writeText(code), 500); }
        catch (e) { fallbackCopy(code); }
      } else {
        fallbackCopy(code);
      }
      const t = b.textContent;
      b.textContent = 'Copied ✓';
      b.classList.add('done');
      setTimeout(() => { b.textContent = t; b.classList.remove('done'); }, 1600);
    }));
  })();

  /* ---------- giveaway countdown ---------- */
  (function countdown() {
    const D = document.getElementById('d'), H = document.getElementById('h'),
          M = document.getElementById('m'), S = document.getElementById('s');
    if (!D || !H || !M || !S) return;

    const enterBtn = document.getElementById('enter');
    const giveCard = document.querySelector('.give');

    function expire() {
      D.textContent = H.textContent = M.textContent = S.textContent = '00';
      if (enterBtn) {
        enterBtn.textContent = 'Winners announced — next giveaway soon';
        enterBtn.classList.add('btn-ghost');
        enterBtn.classList.remove('btn-white');
        enterBtn.setAttribute('aria-disabled', 'true');
        enterBtn.addEventListener('click', (e) => e.preventDefault());
      }
      if (giveCard) giveCard.classList.remove('entry-mode');
    }

    function tick() {
      const ms = GIVEAWAY_END - new Date();
      if (ms <= 0) { expire(); return; }
      let rem = ms;
      const d = Math.floor(rem / 864e5); rem -= d * 864e5;
      const h = Math.floor(rem / 36e5); rem -= h * 36e5;
      const m = Math.floor(rem / 6e4); rem -= m * 6e4;
      const s = Math.floor(rem / 1e3);
      D.textContent = String(d).padStart(2, '0');
      H.textContent = String(h).padStart(2, '0');
      M.textContent = String(m).padStart(2, '0');
      S.textContent = String(s).padStart(2, '0');
      setTimeout(tick, 1000);
    }
    tick();
  })();

  /* ---------- giveaway entry form ---------- */
  (function entryForm() {
    const enterBtn = document.getElementById('enter');
    const give = document.querySelector('.give');
    const form = document.getElementById('entry-form');
    if (!enterBtn || !give || !form) return;

    enterBtn.addEventListener('click', (e) => {
      e.preventDefault();
      give.classList.add('entry-mode');
      form.classList.add('open');
      const firstField = form.querySelector('input:not([type="checkbox"])');
      if (firstField) firstField.focus();
    });

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const msgEl = form.querySelector('.form-msg');
      const submitBtn = form.querySelector('button[type="submit"]');
      const honeypot = form.querySelector('input[name="_gotcha"]');
      if (honeypot && honeypot.value) return; // silently drop bot submissions

      if (submitBtn) submitBtn.disabled = true;
      try {
        const res = await fetch(form.action, {
          method: 'POST',
          body: new FormData(form),
          headers: { Accept: 'application/json' }
        });
        if (res.ok) {
          form.reset();
          form.querySelectorAll('.field, .field-check').forEach((f) => f.style.display = 'none');
          if (submitBtn) submitBtn.style.display = 'none';
          if (msgEl) {
            msgEl.textContent = "You're entered. We'll verify your entry and reach out if you win.";
            msgEl.className = 'form-msg success';
          }
        } else {
          throw new Error('Form submission failed');
        }
      } catch (err) {
        if (msgEl) {
          msgEl.textContent = 'Something went wrong submitting your entry. Please try again.';
          msgEl.className = 'form-msg error';
        }
        if (submitBtn) submitBtn.disabled = false;
      }
    });
  })();
})();
