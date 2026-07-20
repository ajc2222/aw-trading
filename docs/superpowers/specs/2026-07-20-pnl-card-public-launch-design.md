# P&L Card Generator — Public Launch Design

## Context

The P&L Card Generator (`website/pnl-card.html`) is a free tool that lets traders turn their trade data (manual entry or CSV import) into a branded, shareable P&L card. It's currently gated behind a static, hardcoded password (`awtrading2026`) and not linked from anywhere on the public site.

The tool already has virality/lead-gen mechanics built in:
- Every export is permanently watermarked with the AW Trading logo + `joinawtrading.com`
- A post-export share nudge links to Discord and Instagram
- A "Verified from CSV" badge adds credibility to imported (vs. hand-typed) numbers

Right now none of that reaches anyone, because the tool isn't discoverable and the password gate blocks casual visitors. The goal of this change is to make the tool public and use it as a lead magnet for free Discord membership — the site's actual growth constraint — rather than just a UI utility.

## Decisions (from brainstorming)

1. **Gate mechanic:** replace the password gate with an honor-system "Join Discord to unlock" gate. No real membership verification (no OAuth, no backend) — same complexity class as the current password gate, just a different unlock action.
2. **Discoverability:** add a `P&L Cards` link to site navigation (desktop nav, mobile nav, footer) on every public page, pointing to `/pnl-card`.
3. **Scope:** front-end only. No backend, no new infrastructure, no data storage.

## Design

### 1. Nav placement

Add a `P&L Cards` nav link, positioned after "Prop Firms", in:
- `website/index.html` — desktop `.nav-links`, `.mobile-nav-links`, footer `.foot-links`
- `website/indicator.html` — desktop `.nav-links`, `.mobile-nav-links`
- `website/giveaways.html` — desktop `.nav-links`, `.mobile-nav-links` (and footer, if that page has one)

This follows the existing pattern already used for Indicator / Mentorship / Prop Firms — nav is duplicated per-page (no shared component/include system exists in this static site), so each page's markup is edited individually.

Link target: `/pnl-card` (existing route via Vercel clean URLs, same as `/indicator`).

### 2. Replace the password gate

In `website/pnl-card.html`, the `#pw-gate` element and its `checkPw()` script are replaced with a Discord-join gate:

- Same visual shell/positioning (fixed fullscreen overlay, centered card, AW Trading branding) as the current password gate — no new visual system needed.
- Copy:
  - Eyebrow: "AW TRADING"
  - Headline: "Free P&L Card Generator"
  - Subtext: one line pitching the tool (e.g. "Turn your trades into a branded flex card in seconds.")
- Two buttons:
  - Primary: **"Join Discord to unlock"** — opens `https://discord.gg/fn2qjH7MW4` in a new tab (`target="_blank"`). Does NOT unlock the tool by itself (clicking it alone shouldn't be enough, since the tab may not complete the join).
  - Secondary: **"I've already joined — Continue"** — unlocks the tool immediately.
- Both the "Continue" button click AND returning with an existing valid session are handled the same way as today: set a `sessionStorage` flag (rename from the password's stored value to something like `aw-pnl-unlocked`), hide the gate, no page reload needed.
- Remove the hardcoded `PW = 'awtrading2026'` constant and `checkPw()` logic entirely.

### 3. What stays unchanged

- The card generator UI/logic itself (presets, themes, CSV import, export, share nudge, verified badge, background upload/URL) — no changes.
- No new dependencies, no backend routes, no environment variables.

## Testing

Manual verification only (static front-end change):
1. From each page (`/`, `/indicator`, `/giveaways`), click the new `P&L Cards` nav link (desktop and mobile) and confirm it lands on `/pnl-card`.
2. On first visit, confirm the Discord-join gate shows instead of the old password prompt.
3. Confirm "Join Discord to unlock" opens the Discord invite in a new tab and does not unlock the tool on its own.
4. Confirm "I've already joined — Continue" unlocks the tool and hides the gate.
5. Reload the page within the same browser session and confirm the gate does not reappear (sessionStorage persists).
6. Open a fresh/incognito session and confirm the gate reappears.
7. Confirm the tool itself (export, CSV import, share nudge, verified badge) still works unchanged post-unlock.

## Out of scope

- Real Discord membership verification (OAuth) — explicitly deferred; honor-system only for now.
- Email capture as an alternative/additional gate.
- A dedicated marketing landing page separate from the gate screen.
- Adding the nav link to any page not listed above (e.g. `pnl-card.html` itself already has its own back-link to the homepage).
