# AW Trading — Full Project Overview

*Last updated: 2026-07-23*

---

## What Is AW Trading

AW Trading is AJ's trading education and mentorship brand. It teaches ICT (Inner Circle Trader) methodology — focusing on why price does what it does, real price action, and building a personal edge through data. The community lives on Discord (free), and paid products launch September 1, 2026.

**Domain:** joinawtrading.com  
**Discord:** discord.gg/fn2qjH7MW4  
**YouTube:** @AWTradingYT  
**Instagram:** _awtrading  
**Sales platform:** Whop  

---

## Products

### AW Indicator — $39/mo
A TradingView Pine Script indicator (v6) that maps the AW playbook directly on chart. Features:

- **CISD + IFVG** — Change in State of Delivery with Implied Fair Value Gaps
- **Session Liquidity** — key level detection per session
- **HTF FVG** — higher-timeframe fair value gaps drawn down to working chart
- **Trailing Stop** — dynamic stop management
- **EQH / EQL** — equal highs/lows (liquidity magnets)
- **SMT Divergence** — Smart Money Technique divergence across correlated pairs (NQ/ES/etc.)

Separate files: `aw-full-indicator.pine` (combined), `aw-htf-imbalance.pine` (HTF module), `aw-smt-indicator.pine` (SMT module).

Currently: **free early access / beta** while the launch builds.

### Live Trader Mentorship — $129/mo
NOT for beginners. Assumes students know FVGs, BOS, basic ICT. Focus:

- Why price does what it does
- Data collection and building a personal edge
- Psychology — the trader as the variable
- Building discretion

**6 video modules** (filmed weekly every Thursday, Jul–Aug):
1. Why Price Does What It Does
2. Building Your Data Collection System
3. Finding Your Edge in the Data
4. Psychology — Understanding Yourself as the Variable
5. Building Discretion
6. Advanced Concepts — What I've Actually Picked Up

**5 written playbooks:** trade log template, monthly review framework, psychology self-audit, risk/sizing guide, pre-session framework.

**Members-only Discord channels (created Sept 1):** #live-trader-lounge, #trade-alerts, #trade-journal, #resources, #weekly-live, #indicator-users ($39 tier).

---

## Website — awtrading.com

Plain static HTML/CSS/JS. No framework, no build step. Deployed on Vercel.

### Pages
| Route | File | Purpose |
|---|---|---|
| `/` | `index.html` | Home — hero, stats, mentor section, product CTAs |
| `/indicator` | `indicator.html` | AW Indicator landing page + feature breakdown |
| `/prop-firms` | `prop-firms.html` | Partner prop firm affiliate codes |
| `/giveaways` | `giveaways.html` | Giveaway entry form + past winners |
| `/pnl-card` | `pnl-card.html` | P&L gate page |
| `/404` | `404.html` | "This trade got stopped out." |
| `/privacy` | `privacy.html` | Privacy policy |
| `/terms` | `terms.html` | Terms of service |

### Design System
- **Background:** flat `#070709` on every page, every section. No alternation.
- **Color rule:** monochrome at rest, blue (`#2E6BFF`) only on motion/hover/interaction.
- **Typography:** Archivo (display/body, 900wt, tight tracking) + IBM Plex Mono (eyebrows, stats, tickers).
- **Surfaces:** glass cards — `backdrop-filter: blur(18px)`, subtle gradient borders, inset highlights.
- **Animation:** liquid blob background, spinning gradient CTA rings, scroll reveals via IntersectionObserver. All animation respects `prefers-reduced-motion`.
- **Fonts:** self-hosted (latin subset woff2 in `assets/fonts/`).

### Key Technical Choices
- `vercel.json`: `cleanUrls: true`, `trailingSlash: false`
- Single shared `css/styles.css` + `js/main.js` across all pages
- Stripe Payment Links (no backend) for checkout
- Formspree for giveaway entries
- JSON-LD structured data per page (SoftwareApplication on indicator, Organization on home)
- Sitemap + robots.txt

### Placeholder Registry (must fill before Sept 1)
Search for `[` or `data-todo` to find every unfilled placeholder:
- Home stats bar: "500+ traders mentored", "120+ hours" — replace with real numbers
- Hero equity chart: "+38.4R / SIMULATED MODEL" — keep label unless real audited data
- Prop firms: `[Partner Firm 01/02/03]`, codes `AWTRADING`/`AW10`/`AW20`
- Giveaway winners: `[Winner Handle]` ×4
- Stripe Payment Links in `js/main.js` `STRIPE_LINKS` constant
- Formspree form ID on giveaways page
- Mentor section: AW bio + real photo in `.mentor-photo`

---

## Launch Strategy — Sept 1, 2026

8-week pre-launch content campaign starting July 6, 2026.

**Funnel:** YouTube / Instagram → awtrading.com → Discord (free) → Sept 1 purchase

### 8-Week Schedule
| Period | Focus |
|---|---|
| Weeks 1–4 (Jul 6 – Aug 2) | Pure free value. YouTube 1–2×/wk, Instagram 2–3 Reels/wk, Discord #free-education 3×/wk |
| Week 5 (Aug 3–9) | Open #indicator-preview. First tease clips — no price, no name |
| Week 6 (Aug 10–16) | Open #sept-1-launch + #testimonials. Full reveal: $39/$129, Sept 1 date, Whop link |
| Week 7 (Aug 17–23) | Daily indicator clips. Countdown sticker. Build heat |
| Aug 24–31 | Sustain. Draft all launch day posts |
| **Sept 1** | **Launch** — IG Reel 8:30am, Discord 9am, YouTube Live 9:30am |

### Weekly Filming Rhythm
- **Tuesday (2hr):** Batch film all public content (YouTube + Reels)
- **Thursday (1hr):** Film one private membership module + write one playbook PDF
- **Wed–Fri:** Post public content, Discord education drop
- **Sunday:** Metrics review + next week prep

### Website Launch Mechanic
The site has a countdown bar that auto-flips to "now live!" after Sept 1. All pre-launch states are toggled via `LAUNCH:` comments in the HTML — grep for that string to find every flip point.

---

## RAG Discord Bot

Mention-based Q&A bot (`@AW Bot`) for the Discord community. Searches indexed YouTube transcripts from trading educators and answers using LLMs.

**Directory:** `rag-agent/`

### Stack
| File | Role |
|---|---|
| `bot.py` | Discord bot, mention-triggered |
| `ingest.py` | YouTube ingestion (captions → Whisper fallback) |
| `rag.py` | ChromaDB vector store + Gemini embeddings |
| `config.py` | Creator list with playlist URLs |

**LLMs:** Groq (llama-3.3-70b) for generation, Gemini (gemini-embedding-001) for embeddings — both free tier.

### Indexed Creators
| Creator | Status |
|---|---|
| Flux Trades | Needs re-ingest (no timestamps) |
| Aidenomics | Needs re-ingest (no timestamps) |
| BionicNQ | Needs re-ingest (no timestamps) |
| AW Trading | Partial (~7/15 videos) |
| TTrades | Not started (196 videos, needs Whisper) |
| ICT | Not started (41 videos, needs Whisper) |
| GXT | Skipped (captions fully disabled) |

### Deployment
Target: **Oracle Cloud Always Free ARM VM** (24/7, free). Deploy files ready: `setup.sh`, `aw-bot.service` (systemd). Needs GitHub push + VM setup.

---

## Hormozi RAG Web App

A web-accessible (not Discord) RAG chat over all Alex Hormozi content — YouTube + The Game podcast.

**Directory:** `hormozi-rag/`

### Stack
- `ingest.py` — RSS/Whisper for podcast + yt-dlp/transcript API for YouTube
- `rag.py` — ChromaDB + local `all-MiniLM-L6-v2` sentence-transformers
- Planned deployment: Qdrant Cloud (free) + HuggingFace Inference API + Groq + Vercel Next.js chat UI

### Status (as of 2026-07-14)
- Podcast: 853 chunks / 67 of 1135 episodes ingested
- YouTube: not started
- Deployment: pending podcast + YouTube ingest completion

---

## Design System Document

`content/design-system/DESIGN-SYSTEM.md` — full brand and component spec, used as the source of truth for all website work. Covers tokens, typography rules, component recipes (glass cards, buttons, glow rings, liquid layer), and motion guidelines.

---

## Content Notes

`content/content-notes/` contains:
- `daily-bias-video-plan.md` — structure for daily bias YouTube content
- `future-video-concepts.md` — backlog of video ideas
- `teaching-style-notes.md` — how AJ wants to communicate concepts

AJ uses a **slideshow creator tool** for videos. Claude generates slide-by-slide structure (title, bullet, visual direction) as a direct handoff — no narration scripts.

---

## Key File Locations

| What | Where |
|---|---|
| Website | `website/` |
| Shared stylesheet | `website/css/styles.css` |
| Shared JS | `website/js/main.js` |
| Indicator (full) | `indicator/aw-full-indicator.pine` |
| Indicator (HTF) | `indicator/aw-htf-imbalance.pine` |
| Indicator (SMT) | `indicator/aw-smt-indicator.pine` |
| RAG bot | `rag-agent/` |
| RAG progress | `rag-agent/PROGRESS.md` |
| Hormozi RAG | `hormozi-rag/` |
| Design system | `content/design-system/DESIGN-SYSTEM.md` |
| Content notes | `content/content-notes/` |
| Build brief (original) | `CLAUDE-CODE-BRIEF.md` |
| Launch checklist | `website/LAUNCH-CHECKLIST.md` |
