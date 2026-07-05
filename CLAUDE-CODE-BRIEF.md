# AW TRADING — WEBSITE BUILD BRIEF (for Claude Code)

You are building the production website for **AW Trading**, a trading education and mentorship brand. Four HTML prototype files are included in this project folder — they are the **source of truth for design, copy, and layout**. Your job is to turn them into a clean, deployable, production-grade static site.

---

## 0. TECH DECISIONS (already made — do not relitigate)

- **Stack:** Plain static HTML/CSS/JS. No framework. No build step beyond what's listed here. This is a marketing site; keep it fast and simple.
- **Hosting:** Vercel (static deployment).
- **Payments (v1):** Stripe Payment Links (hosted checkout — no backend). CTA buttons link out to Stripe.
- **Forms (v1):** Formspree (or Tally embed) for giveaway entries and contact. No custom backend.
- **Fonts:** Google Fonts — `Archivo` (variable, wdth/wght) + `IBM Plex Mono`. Self-host them at build if easy (fontsource or downloaded woff2) for performance; otherwise keep the Google CDN links.

---

## 1. BRAND DESIGN LAW (non-negotiable)

1. **One background.** Every page, every section: flat `#070709`. No section-to-section color alternation. No grey radial washes behind sections. Depth comes ONLY from card surfaces, borders, and tight shadows.
2. **Monochrome when static, blue when moving.** Everything at rest is black/white/grey. The accent blue `#2E6BFF` appears ONLY on things that move or respond: animations (chart line draw, pulses, underline sweep, count-ups), hover states, focus rings, live indicators.
3. **White carries identity.** Primary buttons, featured plan border, badges, blockquote bars, glows/shadows = white (`rgba(255,255,255,…)`), kept tight (blur ≤ ~40px, strong negative spread) so they never haze the background grey.
4. **Typography:** Archivo for display/body (900 weight, tight tracking, slightly extended for headlines). IBM Plex Mono for eyebrows, tickers, stats labels, fine print.
5. **Design tokens (CSS custom properties):**
   ```css
   --bg:#070709; --card:#0F1013; --white:#F5F6F8; --muted:#8B8F9C;
   --line:rgba(255,255,255,.10); --line-strong:rgba(255,255,255,.22);
   --white-glow:rgba(255,255,255,.10); --white-glow-hard:rgba(255,255,255,.18);
   --blue:#2E6BFF; --blue-glow:rgba(46,107,255,.35);
   ```
6. **Motion rules:** IntersectionObserver scroll reveals (translateY + fade, staggered ~80ms). All animation respects `prefers-reduced-motion`. Never animate layout properties — transform/opacity only.

---

## 2. REPO STRUCTURE (target)

```
aw-trading/
├── index.html              # from aw-trading.html (rename)
├── prop-firms.html
├── indicator.html
├── giveaways.html
├── css/
│   └── styles.css          # ONE shared stylesheet extracted from the four files
├── js/
│   └── main.js             # reveals, count-up, copy-code, countdown, mobile nav
├── assets/
│   ├── favicon.svg         # "AW" mark: white rounded square, black AW, matches .logo-mark
│   ├── og-image.png        # 1200x630, black bg, white "AW Trading" wordmark, blue underline
│   └── fonts/              # if self-hosting
├── vercel.json             # clean-urls: true
└── README.md               # how to edit content, deploy, and update codes/dates
```

## 3. TASKS (in order)

### Phase 1 — Refactor
- [ ] Extract the (currently duplicated) CSS from all four HTML files into one `css/styles.css`. Deduplicate. Page-specific styles stay in the shared file under clear comment headers (`/* == indicator page == */`).
- [ ] Extract all JS into `js/main.js`. Guard each feature so it no-ops if its elements aren't on the page.
- [ ] Rename `aw-trading.html` → `index.html`; update every internal link (`aw-trading.html` → `/`, others → `/prop-firms` etc. with Vercel cleanUrls).
- [ ] Verify: with all pages open side by side, backgrounds are identical flat `#070709`. Any residual grey wash = bug.

### Phase 2 — Gaps the prototypes have (fix them)
- [ ] **Mobile navigation.** Nav links are currently `display:none` under 980px with no replacement. Build a hamburger menu: full-screen overlay, black bg, big Archivo links, blue-accented open/close animation. Keyboard accessible (Esc closes, focus trap).
- [ ] **SEO/meta:** unique `<title>` + meta description per page, Open Graph + Twitter card tags, canonical URLs, `sitemap.xml`, `robots.txt`.
- [ ] **Favicon** + OG image per structure above.
- [ ] **Accessibility pass:** landmarks (`header/main/footer/nav`), skip-to-content link, aria-labels on the ticker (`aria-hidden` is set — keep), contrast check on `--muted` text (bump if it fails AA on `#070709`), visible focus states everywhere.
- [ ] **Performance:** `font-display: swap`, preload the two font files actually used, lazy-load nothing critical (site is light), Lighthouse ≥ 95 on all four categories.

### Phase 3 — Functionality
- [ ] **Stripe Payment Links:** wire the three membership CTAs (index) and the two indicator CTAs to placeholder constants at the top of `main.js` or as `data-` attributes — one obvious place to paste real Stripe URLs. Buttons with placeholder links get `data-todo="stripe"` and a console.warn in dev.
- [ ] **Giveaway entry:** replace the `#enter` anchor with a Formspree form (name, email, social handle, checkbox agreeing to official rules). Inline success state, no redirect. Honeypot field for spam.
- [ ] **Countdown:** keep the existing logic; move the `END` date to a single config constant at the top of `main.js` with a loud comment. When expired, swap the card CTA to "Winners announced — next giveaway soon."
- [ ] **Copy-code buttons** (prop-firms): keep behavior; add clipboard fallback for non-secure contexts.
- [ ] **404 page** in the same design language. Headline: "This trade got stopped out." CTA back home.

### Phase 4 — Deploy
- [ ] `vercel.json` with `{ "cleanUrls": true, "trailingSlash": false }`.
- [ ] Deploy to Vercel, verify all routes, run Lighthouse, fix regressions.

---

## 4. CONTENT — PLACEHOLDER REGISTRY (do not invent real data)

These are intentionally fake/placeholder. Keep them clearly marked; the owner replaces them before launch. **Never fabricate real firm names, winner names, or performance stats.**

| Location | Placeholder | Owner must supply |
|---|---|---|
| index stats bar | "500+ traders mentored", "120+ hours" | Real numbers or delete |
| index hero chart | "+38.4R / SIMULATED MODEL" | Keep "SIMULATED" label unless real audited data |
| prop-firms cards | `[Partner Firm 01-03]`, codes AWTRADING/AW10/AW20 | Real partner names, real codes, real % |
| giveaways winners | `[Winner Handle]` ×4 | Real verified winners |
| giveaways countdown | `2026-07-31T20:00` | Real draw date |
| mentor section | AW bio copy | Real story + real photo (drop into `.mentor-photo`) |
| footer | Terms/Privacy `#` links | Real legal pages |

## 5. COMPLIANCE (keep these — they are load-bearing)

- Risk disclosure block in the footer of index (and add a condensed one-liner + link to full disclosure in the footers of the other three pages).
- Affiliate disclosure on prop-firms.
- "No purchase necessary" official-rules summary on giveaways.
- Indicator page must keep honest framing: analysis tool, no profit guarantees.
- Never add earnings claims, win-rate claims, or "guaranteed funding" copy anywhere.

## 6. ACCEPTANCE CRITERIA

1. All four pages + 404 share one stylesheet, one JS file, identical flat-black background, identical nav/footer.
2. Blue appears only on motion/interaction; nothing blue at rest.
3. Fully responsive 320px → 1440px; working mobile nav.
4. Lighthouse ≥ 95 across the board on the deployed Vercel URL.
5. Reduced-motion users get a complete, static, readable experience.
6. Every placeholder from §4 is findable by grepping `[` or `data-todo`.
