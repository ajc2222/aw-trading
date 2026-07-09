# Sept 1 Launch Checklist

Run this to find every marker: `grep -rn "LAUNCH:" *.html`

---

## index.html

### 1. Indicator section CTA
Find the `<!-- LAUNCH: -->` comment above the button in `#indicator`.
Replace:
```html
<a href="https://discord.gg/fn2qjH7MW4" target="_blank" rel="noopener" class="btn btn-white">Coming Sept 1 — Join Early <span class="arrow">→</span></a>
```
With:
```html
<a href="/indicator" class="btn btn-white">Get The Indicator <span class="arrow">→</span></a>
```

### 2. Mentorship section
Find the `<!-- LAUNCH: -->` comment above `<section id="mentorship">`.
Replace the entire coming-soon block with the full application form (check git history — commit before 2026-07-09).

---

## indicator.html

### 3. Buy / pricing section
Find the `<!-- LAUNCH: -->` comment above `<section id="buy">`.
Replace the coming-soon block with the two-plan pricing grid:
- **Indicator Only** — $39/mo — button links to `https://whop.com/aw-trading-discord`
- **Live Trader** — $129/mo — button links to `https://whop.com/aw-trading-discord`

(Check git history for the full markup.)

---

## prop-firms.html

### 4. Coming-soon banner
Find the `<!-- LAUNCH: Remove this coming-soon banner section entirely -->` comment.
Delete the entire `<section style="padding-bottom:0">` block (the info bar above the firm cards).

### 5. Firm code buttons — 6 firms
Find all `<!-- LAUNCH: Remove the span below and uncomment the button -->` comments.
For each of the 6 firms:
1. Delete the `<span>Coming Sept 1</span>` line
2. Uncomment the `<button class="buy" data-code="AWTRADING" ...>` line below it

Firms: Lucid Trading, Tradeify, Apex, Alpha Futures, My Funded Futures, Take Profit Trader.
