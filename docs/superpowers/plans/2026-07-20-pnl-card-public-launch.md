# P&L Card Public Launch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the P&L Card Generator publicly reachable from site navigation, gated by an honor-system "join our free Discord" screen instead of the current hardcoded password.

**Architecture:** Pure static-site edit. No backend, no build step, no test framework — this is plain HTML/CSS/JS served by Vercel. Verification is manual, via a local static file server (`npx serve`) and a browser.

**Tech Stack:** HTML, CSS, vanilla JS. No new dependencies.

## Global Constraints

- No backend, no OAuth, no membership verification — honor-system gate only (per spec §"Decisions").
- Discord invite URL: `https://discord.gg/fn2qjH7MW4` (already used elsewhere in the codebase — reuse verbatim).
- Gate unlock must persist for the browser session via `sessionStorage`, using key `aw-pnl-unlocked` with value `'1'` (renamed from the old `aw-auth`/password-value pair).
- Nav link label: exactly `P&L Cards`, target `/pnl-card`.
- Nav link position: immediately after the `Prop Firms` link, in every nav list it's added to (desktop nav, mobile nav, footer).
- Remove the old `PW` constant, `checkPw()` function, and `#pw-input`/`#pw-err` elements entirely — no dead code left behind.
- No changes to the card generator's own functionality (presets, CSV import, export, share nudge, verified badge, background upload/URL).

---

### Task 1: Replace the password gate with a Discord-join gate

**Files:**
- Modify: `website/pnl-card.html:384-404`

**Interfaces:**
- Produces: gate now unlocks via `unlockGate()` (global function) instead of `checkPw()`. Session flag is `sessionStorage['aw-pnl-unlocked'] === '1'`. No other file depends on this.

- [ ] **Step 1: Replace the gate markup and script**

Open `website/pnl-card.html`. Find lines 384-404 (the `<!-- ── Password gate ── -->` comment through the closing `</script>` of the password-check script). Replace that entire block with:

```html
<!-- ── Discord-join gate ── -->
<div id="pw-gate" style="position:fixed;inset:0;z-index:9999;background:#070709;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:16px;font-family:'IBM Plex Mono',monospace;padding:24px;text-align:center">
  <div style="font-size:.65rem;letter-spacing:.2em;text-transform:uppercase;color:#6A6F7C">AW Trading</div>
  <div style="font-size:1.3rem;font-weight:600;color:#F5F6F8;font-family:'Archivo',sans-serif;letter-spacing:-.01em">Free P&amp;L Card Generator</div>
  <div style="font-size:.78rem;color:#9298A6;font-family:'Archivo',sans-serif;max-width:280px;line-height:1.5">Turn your trades into a branded flex card in seconds.</div>
  <div style="height:1px;width:180px;background:rgba(255,255,255,.07);margin:4px 0"></div>
  <a href="https://discord.gg/fn2qjH7MW4" target="_blank" rel="noopener"
    style="background:#2E6BFF;color:#fff;border:none;border-radius:8px;padding:10px 28px;font-family:inherit;font-size:.78rem;cursor:pointer;letter-spacing:.06em;font-weight:600;text-decoration:none;display:inline-block">Join Discord to unlock</a>
  <button onclick="unlockGate()" style="background:transparent;color:#9298A6;border:1px solid rgba(255,255,255,.12);border-radius:8px;padding:9px 22px;font-family:inherit;font-size:.72rem;cursor:pointer;letter-spacing:.04em">I've already joined — Continue</button>
</div>
<script>
(function(){if(sessionStorage.getItem('aw-pnl-unlocked')==='1')document.getElementById('pw-gate').style.display='none';})();
function unlockGate(){
  sessionStorage.setItem('aw-pnl-unlocked','1');
  document.getElementById('pw-gate').style.display='none';
}
</script>
```

This removes the `<input id="pw-input">`, `<div id="pw-err">`, `const PW`, and `checkPw()` entirely — nothing in the rest of the file references them (confirm with the grep in Step 2).

- [ ] **Step 2: Verify no leftover references**

Run:
```bash
grep -n "checkPw\|pw-input\|pw-err\|aw-auth\|const PW" website/pnl-card.html
```
Expected: no output (all four are gone).

- [ ] **Step 3: Manual verification in a browser**

```bash
cd website && npx --yes serve -l 5500 .
```
Open `http://localhost:5500/pnl-card` in a browser and confirm:
1. The gate shows "Free P&L Card Generator" with the two buttons — no password field.
2. Clicking "Join Discord to unlock" opens the Discord invite in a new tab and the gate stays visible (tool is NOT unlocked yet).
3. Clicking "I've already joined — Continue" hides the gate and the tool is usable.
4. Reload the page (same tab/session) — gate does not reappear.
5. Open the URL in a new Incognito window — gate reappears (fresh session).

Stop the server (`Ctrl+C` or kill the background process) once confirmed.

- [ ] **Step 4: Commit**

```bash
git add website/pnl-card.html
git commit -m "$(cat <<'EOF'
feat: replace P&L card password gate with Discord-join gate

Makes the tool safe to link publicly. Honor-system only (no
membership verification) — clicking through unlocks the tool, same
trust model as the password gate it replaces.
EOF
)"
```

---

### Task 2: Add "P&L Cards" nav link across the public site

**Files:**
- Modify: `website/index.html:349,384,669`
- Modify: `website/indicator.html:296,318,492`
- Modify: `website/giveaways.html:233,266,362`

**Interfaces:**
- Consumes: `/pnl-card` route (now public as of Task 1 — the gate no longer requires a password, so linking to it is safe).
- Produces: none (leaf UI change, nothing else depends on this).

- [ ] **Step 1: Add the link to `website/index.html`**

Desktop nav — at line 349, insert immediately after the `Prop Firms` link so the block reads:

```html
      <a href="#indicator">Indicator</a>
      <a href="#mentorship">Mentorship</a>
      <a href="#prop-firms">Prop Firms</a>
      <a href="/pnl-card">P&amp;L Cards</a>
```

Mobile nav — at line 384, insert after `Prop Firms` so the block reads:

```html
    <a href="/">Home</a>
    <a href="/indicator">Indicator</a>
    <a href="/#mentorship">Mentorship</a>
    <a href="/prop-firms">Prop Firms</a>
    <a href="/pnl-card">P&amp;L Cards</a>
```

Footer — at line 669, insert after `Prop Firms` so the block reads:

```html
        <a href="/indicator">Indicator</a>
        <a href="/#mentorship">Mentorship</a>
        <a href="/prop-firms">Prop Firms</a>
        <a href="/pnl-card">P&amp;L Cards</a>
        <a href="/terms">Terms</a>
```

- [ ] **Step 2: Add the link to `website/indicator.html`**

Desktop nav — at line 296, insert after `Prop Firms`:

```html
      <a href="/indicator" class="on" aria-current="page">Indicator</a>
      <a href="/#mentorship">Mentorship</a>
      <a href="/prop-firms">Prop Firms</a>
      <a href="/pnl-card">P&amp;L Cards</a>
```

Mobile nav — at line 318, insert after `Prop Firms`:

```html
    <a href="/">Home</a>
    <a href="/indicator" aria-current="page">Indicator</a>
    <a href="/#mentorship">Mentorship</a>
    <a href="/prop-firms">Prop Firms</a>
    <a href="/pnl-card">P&amp;L Cards</a>
```

Footer — at line 492, insert after `Prop Firms`:

```html
      <a href="/indicator">Indicator</a>
      <a href="/#mentorship">Mentorship</a>
      <a href="/prop-firms">Prop Firms</a>
      <a href="/pnl-card">P&amp;L Cards</a>
      <a href="/terms">Terms</a>
```

- [ ] **Step 3: Add the link to `website/giveaways.html`**

Desktop nav — at line 233, insert after `Prop Firms`:

```html
      <a href="/">Home</a>
      <a href="/#pricing">Membership</a>
      <a href="/indicator">Indicator</a>
      <a href="/#mentorship">Mentorship</a>
      <a href="/prop-firms">Prop Firms</a>
      <a href="/pnl-card">P&amp;L Cards</a>
```

Mobile nav — at line 266, insert after `Prop Firms` (before the existing `Giveaways` self-link):

```html
    <a href="/">Home</a>
    <a href="/indicator">Indicator</a>
    <a href="/#mentorship">Mentorship</a>
    <a href="/prop-firms">Prop Firms</a>
    <a href="/pnl-card">P&amp;L Cards</a>
    <a href="/giveaways" aria-current="page">Giveaways</a>
```

Footer — at line 362, insert after `Prop Firms`:

```html
      <a href="/">Home</a>
      <a href="/prop-firms">Prop Firms</a>
      <a href="/pnl-card">P&amp;L Cards</a>
      <a href="/indicator">Indicator</a>
      <a href="/terms">Terms</a>
```

- [ ] **Step 4: Verify the links are present everywhere**

Run:
```bash
grep -rn 'href="/pnl-card"' website/index.html website/indicator.html website/giveaways.html
```
Expected: 9 lines total (3 per file — desktop nav, mobile nav, footer).

- [ ] **Step 5: Manual verification in a browser**

```bash
cd website && npx --yes serve -l 5500 .
```
For each of `http://localhost:5500/`, `http://localhost:5500/indicator`, `http://localhost:5500/giveaways`:
1. Confirm "P&L Cards" appears in the desktop nav (or resize/use devtools mobile view to check the mobile nav) after "Prop Firms".
2. Click it and confirm it lands on `/pnl-card` and shows the Discord-join gate from Task 1.
3. Scroll to the footer and confirm "P&L Cards" appears there too, and links correctly.

Stop the server once confirmed.

- [ ] **Step 6: Commit**

```bash
git add website/index.html website/indicator.html website/giveaways.html
git commit -m "$(cat <<'EOF'
feat: add P&L Cards nav link across public site

Surfaces the P&L card generator (now public via the Discord-join
gate) in desktop nav, mobile nav, and footer on the homepage,
indicator page, and giveaways page.
EOF
)"
```

---

### Task 3: Push to production

**Files:** none (deployment step)

**Interfaces:** none

- [ ] **Step 1: Confirm branch is clean and up to date**

```bash
git status
git log origin/master..HEAD --oneline
```
Expected: working tree clean, and the two commits from Tasks 1–2 listed as ahead of `origin/master`.

- [ ] **Step 2: Push**

```bash
git push origin master
```

- [ ] **Step 3: Post-deploy smoke check**

Once Vercel finishes deploying (check the Vercel dashboard or wait ~1 minute), repeat the manual verification from Task 2 Step 5 against the real production domain instead of localhost, to confirm the deployed version behaves the same way.
