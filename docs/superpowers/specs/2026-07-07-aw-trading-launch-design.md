# AW Trading — Sept 1 Launch Business Design

**Date:** 2026-07-07  
**Launch target:** September 1, 2026  
**Products:** AW Indicator ($39/mo) · Live Trader mentorship ($129/mo)  
**Sales platform:** Whop  
**Community:** Discord (discord.gg/fn2qjH7MW4)

---

## 1. Strategy Overview

**Chosen approach: Full Launch System (Option C)**

Focus on content-first audience growth (YouTube + Instagram) driving free Discord membership, then nurturing that community through an 8-week runway into a Sept 1 paid product launch. No email capture. No paid ads. Social proof via existing P&L screenshots, certifications, and prop firm passes.

**Core funnel:**
```
YouTube / Instagram (free value)
  → website (awtrading.com)
    → Discord (free community via Whop)
      → Sept 1: indicator purchase on Whop
```

---

## 2. Website Changes (Implemented)

All changes were applied to `index.html`, `indicator.html`, `prop-firms.html`, `giveaways.html`, `terms.html`, `privacy.html`, and `css/styles.css`.

### Social links
- YouTube (`@AWTradingYT`) and Instagram (`_awtrading`) icons added to nav bar (desktop, hidden mobile) and footer across all pages
- JSON-LD `sameAs` on homepage updated to include both platforms + Discord

### Launch countdown bar
- Persistent banner below nav on all 4 main pages
- Real-time JS countdown to `2026-09-01T00:00:00Z`
- CTA copy: "AW Indicator + Live Trader launch Sept 1 — join the community free now"
- Auto-replaces with "now live!" text after launch date passes

### SEO (homepage)
- JSON-LD structured data with `sameAs` social links
- Hero and meta tags were already optimized in a prior session

---

## 3. Discord Nurture Flow (8 Weeks)

### New channels to create
| Channel | Purpose | When to add |
|---|---|---|
| `#indicator-preview` | Teaser screenshots and clips | Week 5 |
| `#sept-1-launch` | Countdown, pricing announcement, Whop link | Week 6 |
| `#testimonials` | Permanent pin: P&L screenshots, certs, student wins | Week 6 |

Existing channels (`#start-here`, `#free-education`, `#trade-breakdowns`) remain the primary value delivery engine weeks 1–4.

### Member journey

| Step | Timing | Action |
|---|---|---|
| 1 | Day 0 (join) | Auto-welcome → points to `#free-education` and `#trade-breakdowns`. No pitch. |
| 2 | Weeks 1–4 | 3–5× weekly posts in `#free-education`. Concept breakdowns, session recaps, annotated charts. Cross-post YouTube links. |
| 3 | Week 5 | Open `#indicator-preview`. Drop 3 teaser clips — indicator drawing levels, A+ signal firing. No price yet. |
| 4 | Week 6 | Open `#sept-1-launch`. Full announcement: Sept 1 date, $39/mo and $129/mo pricing, Whop link pinned. First hard CTA in 6 weeks. |
| 5 | Week 7 | Daily indicator clip in `#indicator-preview`. Populate `#testimonials` with P&L and certs. Engagement post: "who's grabbing it Sept 1?" |
| 6 | Sept 1 | Multi-channel announcement (`#general`, `#sept-1-launch`, `#start-here`). YouTube/Discord live session. Direct Whop link everywhere. |

---

## 4. Content Calendar (YouTube + Instagram)

### Platform roles
- **YouTube** — authority and trust. 1–2 longer-form videos per week + Shorts. Primary education engine.
- **Instagram** — reach and discovery. 2–5 Reels per week + Stories. Drives traffic to YouTube and Discord.

### 8-Week Schedule

**Week 1 — Jul 6–12 — Establish authority**
- YouTube: "What is ICT and why does it actually work?" (12–15 min). Discord CTA in description.
- Instagram: 2 Reels (ICT terms, P&L screenshot). 1 Story poll.

**Week 2 — Jul 13–19 — Teach a system**
- YouTube: Full NY open trade breakdown (long) + 1 Short clipped from it.
- Instagram: 2 Reels (A+ setup, cert/prop pass). Story driving to YouTube.

**Week 3 — Jul 20–26 — Social proof + education**
- YouTube: "How I find liquidity grabs before they happen" (10–18 min).
- Instagram: 2 Reels (prop eval pass, YouTube clip hook). Story: Q&A sticker collecting audience trading struggles (use responses in Week 6 objection content).

**Week 4 — Jul 27–Aug 2 — Community + live value**
- YouTube: Weekly recap vlog + 1 Short from a live trade clip.
- Instagram: 2 Reels (Discord server tour, trading mistake). Story: soft tease "something big in 4 weeks."

**Week 5 — Aug 3–9 — First indicator tease**
- YouTube: "I've been building something…" — 10 sec clip of indicator on live chart, no name or price. Let curiosity drive comments.
- Instagram: 2 Reels (screen recording of levels auto-drawing, signal + result). Story: "Discord members find out first."

**Week 6 — Aug 10–16 — Announce pricing and date**
- YouTube: Full reveal video (15–20 min) — all features live, Sept 1 date, $39/$129 pricing, link to /indicator. Most important video of the 8 weeks.
- Instagram: 2 Reels (announcement Reel + objection-flip using Week 3 Q&A data). 3-part Story series → Discord CTA.

**Week 7 — Aug 17–23 — Build heat**
- YouTube: Raw live trade session using the indicator (uncut) + Short "why I built this."
- Instagram: Daily indicator clips (15–30 sec each). "Is $39/mo worth it?" objection Reel. Instagram countdown sticker to Sept 1 (followers subscribe for launch notification).

**Week 8 / Launch Day — Sept 1**
- YouTube: Go live on launch morning. Show indicator trading the open (30–60 min). Drop Whop link in chat every 10 min. Clip best 2-min segment for a Short immediately after.
- Instagram: Morning Reel at 8:30am ("It's live — link in bio"). Midday clip from the stream. Story every 2 hours all day: member count, live clips, Whop link.
- Discord: Simultaneous announcement in `#general`, `#sept-1-launch`, `#start-here`.

### Minimum viable posting schedule
If bandwidth is tight, the floor is: **1 YouTube video + 2 Instagram Reels per week**. Weeks 5–7 push harder — those are non-negotiable for conversion.

---

## 5. Success Metrics

| Metric | Target by Sept 1 |
|---|---|
| Discord members | 200+ (free tier) |
| YouTube subscribers | Growing week-over-week (views > subs as leading indicator) |
| Instagram Reels reach | 1K+ views per Reel by Week 5 |
| Indicator page `/indicator` visits | Track via Vercel analytics |
| Day-1 Whop conversions | 10+ (realistic for a warmed community of 200+) |

---

## 6. Open Items

- [ ] Publish indicator and Live Trader products on Whop on Sept 1
- [ ] Verify Instagram countdown sticker feature is available on your account
- [ ] Record first YouTube video (Week 1 starts Jul 6 — this week)
- [ ] Create `#indicator-preview`, `#sept-1-launch`, `#testimonials` channels in Discord before Week 5 (Aug 3)
- [ ] Pin Whop link in `#sept-1-launch` when it goes live
