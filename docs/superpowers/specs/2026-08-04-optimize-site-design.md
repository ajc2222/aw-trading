# optimize-site skill — Design Spec

**Date:** 2026-08-04  
**Skill trigger:** `/optimize-site`  
**Purpose:** Closed-loop conversion optimization for joinawtrading.com — pull analytics, diagnose the weakest conversion point, propose and implement targeted changes, deploy, and record everything for the next run.

---

## Goals

Primary metric: **conversions** — Discord free community joins and indicator purchases.

The skill does not optimize for traffic volume or general engagement. Every proposed change must have a clear hypothesis connecting it to one of those two conversion actions.

---

## Conversion targets

| Target | Proxy metric |
|---|---|
| Discord join | `cta_click` custom event with `target: discord` (Vercel Analytics) |
| Indicator purchase | `cta_click` custom event with `target: indicator` + `/indicator` page visits |

Both are tracked via Vercel Analytics custom events using `va('track', ...)` calls on every relevant CTA across the site. If these events are not yet instrumented on the first run, instrumenting them is the first change the skill makes (before any conversion-focused change).

---

## Flow

### Phase 1 — Pull & compare
Query Vercel Analytics via MCP:
- Last 7 days: pageviews by page, referrer breakdown, `cta_click` event counts by target
- Prior 7 days: same dimensions for comparison
- Read `website/.optimize-log.json` to get the baseline from the previous run and what change was made

### Phase 2 — Evaluate last change
If a previous run exists, the skill leads with a verdict before proposing anything new:
- **Improved:** metrics moved in the right direction → proceed to next optimization
- **Declined:** metrics dropped → flag it, recommend reverting the previous change first, give the user the choice
- **Neutral / inconclusive:** flag it, note it in `.optimize-notes.md`, proceed to next hypothesis

### Phase 3 — Diagnose
Identify the single weakest conversion point by examining:
1. Home page → `/indicator` visit ratio (purchase funnel drop-off)
2. `cta_click` event rate for Discord vs total home visitors
3. Referrer mix — if Instagram is sending traffic but Discord clicks are low, the Instagram landing experience is the problem
4. Repeat visit rate on `/pnl-card` — high engagement tool, potential Discord upsell surface

The skill picks **one bottleneck** to address per run. It does not scatter changes across the site.

### Phase 4 — Propose
Present 1–2 specific changes with:
- What file and element will change
- The hypothesis (why this should move the target metric)
- Expected impact (directional, not a precise number)
- Change category: copy (autonomous) or layout (needs local preview)

Wait for user approval before proceeding. User can approve, reject, or modify.

### Phase 5 — Implement
- Create a branch: `optimize/YYYY-MM-DD`
- Make the approved edits to HTML files
- If any layout change is included: start a local preview server, wait for explicit user sign-off before continuing
- `git commit` with a descriptive message referencing the hypothesis
- `vercel --prod` to ship to production

### Phase 6 — Record
After deploy:
- Update `website/.optimize-log.json` with current 7-day metrics snapshot, branch name, and what was changed
- Append a new entry to `website/.optimize-notes.md` with full run notes

---

## Guardrails

| Change type | Autonomy |
|---|---|
| CTA button copy | Autonomous |
| Headline / subheadline copy | Autonomous |
| Urgency / social proof copy | Autonomous |
| Pricing copy ($39 / $129) | Must propose, user approves |
| CTA button placement / layout tweaks | Must propose + local preview before deploy |
| Page structure (add/remove sections) | Must propose + local preview before deploy |
| Brand colors, fonts, logo | Never |
| External URLs (Discord, Whop, indicator links) | Never |

---

## Persistent files

### `website/.optimize-log.json`
Machine-readable state for the skill. Updated after every run.

```json
{
  "lastRun": "2026-08-04T00:00:00Z",
  "branch": "optimize/2026-08-04",
  "change": {
    "file": "website/index.html",
    "description": "Changed primary Discord CTA from 'Join Free' to 'Join 500+ Traders Free'",
    "hypothesis": "More specific social proof in CTA copy increases click-through"
  },
  "baselineMetrics": {
    "period": "2026-07-28 to 2026-08-04",
    "homeVisitors": 120,
    "indicatorVisits": 18,
    "discordClicks": 9,
    "indicatorClicks": 4,
    "topReferrer": "l.instagram.com"
  }
}
```

### `website/.optimize-notes.md`
Human-readable run log. Skill reads this at the start of every run as a reference for what has been tried. Each entry appended chronologically.

```markdown
## 2026-08-04 — optimize/2026-08-04

**Change:** Discord CTA copy on home page hero
**Hypothesis:** Specific social proof ("500+ traders") increases click intent
**Before:** 9 Discord clicks / 120 home visitors (7.5%)
**After:** TBD — evaluate next run

---
```

After evaluation on the next run, the TBD line is filled in with the verdict.

---

## Branch strategy

Each optimization run lives on its own git branch (`optimize/YYYY-MM-DD`). The branch is pushed to GitHub after deploy. On the next run:

- If the change helped → merge branch into `main`
- If it hurt or was neutral → skill flags it; user can revert via Vercel deployment history (instant) or by checking out the previous optimize branch and redeploying

Main stays clean. Each optimize branch is a named checkpoint in GitHub history.

---

## What the skill does NOT do

- Does not run A/B tests simultaneously (one change at a time, clean before/after)
- Does not touch Google Analytics or attempt to read GA4 data
- Does not propose changes to pages other than the one identified as the bottleneck
- Does not merge branches automatically — always a manual step
- Does not generate new assets (images, videos)

---

## First-run setup

On the very first invocation, before any conversion-focused change:
1. Check if `va('track', ...)` calls exist on Discord and indicator CTAs across all pages
2. If not: add Vercel Analytics event instrumentation as the sole change for this run
3. Deploy, record baseline, note in `.optimize-notes.md` that this was a setup run
4. Next run will have real click data to analyze

---

## Scheduling

The skill is designed to be wrapped in a `/schedule` routine. Recommended cadence: every 7 days. The skill is self-contained — each run reads its own state from `.optimize-log.json` and `.optimize-notes.md`, so no session context is needed between runs.
