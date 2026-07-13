# P&L Card Generator — Session Notes

## What We Built

Self-contained tool at `website/pnl-card.html`. Password-gated (`awtrading2026` — change in `const PW` near top of file).

### Features
- **CSV import** (Tradovate format) — auto-fills P&L, RR, Points, ticker, contracts, entry/exit prices
- **5 card presets** — Summary, Detail, Flex, Badge, Grid
- **2 layouts** — Square (1080×1080), Story (675×1200)
- **8 color templates** — AW, Blueprint, Neon, Ember, Gold, Crimson, Violet, Minimal (each sets its own bg gradient + accent + text colors)
- **RR pill** — sits below P&L number, auto-formats to `X.XXR`, hides RR from stats bar when shown, centered in Flex layout
- **P&L color** follows theme accent (not hardcoded green)
- **Background image upload** with overlay dim control
- **Export PNG** + **Copy Image** (Clipboard API)
- **AW logo** preloaded as data URL (fetch → FileReader, avoids CORS canvas taint)
- **html2canvas self-hosted** at `./assets/html2canvas.min.js` (CDN was blocked by CSP)

### Key Fixes Made
- CSP blocked CDN script → self-hosted html2canvas
- Parent `transform: scale()` on preview container corrupted canvas capture → reset to `scale(1)` before export
- Root-relative `/assets/` paths broke on deployed subdirectory → changed to `./assets/`
- `allowTaint:true` tainted canvas and silently broke `toDataURL()` → removed

---

## Potential Improvements

### Export
- **PDF export** — single button that wraps the PNG in a one-page PDF (jsPDF, also self-hostable)
- **Batch export** — export all presets at once as a zip

### Card Design
- **Win/Loss indicator pill** — small "W" or "L" badge like the LONG pill in the Tradesake reference
- **Win rate display** — parsed from CSV but not shown on any card currently
- **Customisable stat labels** — let user rename "Accounts Copied" to whatever they want
- **More font options** — toggle between Archivo and a serif/display font for variety

### CSV / Data
- **Multi-session support** — import multiple days and pick which session to card-ify
- **Broker format presets** — Tradovate detected automatically; could add TopstepX, Apex, FTMO column mappings
- **Points sign** — currently always positive sum of (exit − entry); should respect direction (long vs short)

### UX
- **Password change in UI** — currently requires editing the file directly
- **Preset thumbnails** — small visual preview of each card style in the picker
- **Share link** — encode card state as a URL hash so it can be shared and re-opened
- **Mobile view** — sidebar collapses; preview fills screen
