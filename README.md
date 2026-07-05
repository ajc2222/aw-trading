# AW Trading — Website

Static marketing site. Plain HTML/CSS/JS, no build step, deployed on Vercel.

## Structure

```
aw-trading/
├── index.html          # Home
├── prop-firms.html      → /prop-firms
├── indicator.html       → /indicator
├── giveaways.html        → /giveaways
├── 404.html
├── css/styles.css       # single shared stylesheet
├── js/main.js           # single shared script, config constants at the top
├── assets/
│   ├── favicon.svg
│   ├── og-image.png
│   └── fonts/           # self-hosted Archivo + IBM Plex Mono (latin subset)
├── vercel.json
├── sitemap.xml
└── robots.txt
```

`vercel.json` has `cleanUrls: true`, so `prop-firms.html` is served at `/prop-firms`, etc. Always link with the extension-less path (`/prop-firms`, not `/prop-firms.html`).

## Before launch — things the owner must supply

Search the codebase for `[` (square-bracket placeholders) and `data-todo` — every one of these needs a real value before going live.

1. **Domain.** Replace `https://awtrading.com` in every `<link rel="canonical">`, `og:*`/`twitter:*` meta tag, `sitemap.xml`, and `robots.txt` with the real production domain.
2. **Stripe Payment Links** — `js/main.js`, top of file, `STRIPE_LINKS` object. Paste the real Stripe Payment Link URL for each of the 5 keys. Until replaced, those buttons carry `data-todo="stripe"` and log a `console.warn` in the browser console.
3. **Formspree form** — `giveaways.html`, the `<form id="entry-form">` element. Replace `action="https://formspree.io/f/REPLACE_WITH_FORM_ID"` with your real Formspree endpoint (or swap for a Tally embed). Flagged with `data-todo="formspree"`.
4. **Giveaway countdown** — `js/main.js`, `GIVEAWAY_END` constant near the top. Update every time you run a new giveaway cycle. When the date passes, the entry CTA automatically swaps to "Winners announced — next giveaway soon" and the entry form/countdown hide.
5. **Content placeholders** (never fabricate real values for these):
   - Home page stats bar: "500+ traders mentored", "120+ hours" — replace with real numbers or delete the stat.
   - Home page hero equity chart: keep the "SIMULATED MODEL" label unless the P&L is real, audited trading data.
   - `prop-firms.html`: `[Partner Firm 01/02/03]` names, and the `AWTRADING` / `AW10` / `AW20` codes + discount percentages — replace with real partner names, codes, and offers.
   - `giveaways.html`: `[Winner Handle]` × 4 — replace with real, verified winners. Also confirm the prize copy and official rules match your actual terms.
   - Mentor section (home page): replace the AW bio copy with the real story, and drop a real photo into `.mentor-photo` (currently a placeholder "AW" watermark).
   - Footer `Terms` / `Privacy` links currently point to `/terms` and `/privacy` — these pages don't exist yet; add them or point elsewhere.
6. **Favicon / OG image** — `assets/favicon.svg` and `assets/og-image.png` are functional placeholders in the brand system (white "AW" mark, black background, blue underline). Swap for final brand assets if the owner wants something more custom.

## Editing content

All copy lives directly in the HTML files — there's no CMS or templating. Edit the relevant `.html` file directly. Shared visual styles live in `css/styles.css`, organized under comment headers per page (`/* == indicator page == */` etc.) — don't duplicate CSS into a page's `<head>`.

## Editing behavior

All JS lives in `js/main.js`, organized as small guarded IIFEs — each feature checks for its own DOM elements and no-ops if they're not present on the current page, so the same file is safe to include on every page. Config constants (Stripe links, giveaway end date) are called out at the top of the file with loud comments.

## Deploying

```
vercel --prod
```

Or connect the repo in the Vercel dashboard for git-based deploys. No build command or output directory needed — it's a static site.

After deploying, run Lighthouse against the live URL and confirm all four categories (Performance, Accessibility, Best Practices, SEO) are ≥ 95. Check all routes including `/some-nonexistent-page` to confirm the custom 404 renders.
