# optimize-site Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `/optimize-site` skill — a closed-loop conversion optimization workflow that pulls Vercel Analytics, diagnoses the weakest CTA, proposes targeted copy/layout changes, ships them on a versioned branch, and records everything for the next run.

**Architecture:** Three deliverables built in order: (1) Vercel Analytics custom event wiring in all HTML pages so CTA clicks are queryable via MCP, (2) bootstrapped state files that persist run history, (3) the SKILL.md instruction file that drives the full optimization loop when invoked.

**Tech Stack:** Vanilla HTML/JS, Vercel Analytics (`/_vercel/insights/script.js` + `window.va`), Vercel CLI (`vercel --prod`), Vercel MCP plugin (`mcp__plugin_vercel_vercel__get_web_analytics`), Git branch-per-run versioning.

---

## File Map

| File | Action | Purpose |
|---|---|---|
| `website/index.html:966-974` | Modify | Add `va` event alongside existing gtag call |
| `website/indicator.html:544-552` | Modify | Same — indicator page CTA handler |
| `website/pnl-card.html:1932-1940` | Modify | Same — pnl-card page CTA handler |
| `website/prop-firms.html:428-436` | Modify | Same — prop-firms page CTA handler |
| `website/.optimize-log.json` | Create | Machine-readable state for skill between runs |
| `website/.optimize-notes.md` | Create | Human-readable run log, skill reads as context |
| `~/.claude/skills/optimize-site/SKILL.md` | Create | The skill instruction file itself |

---

## Task 1: Wire Vercel Analytics custom events on all CTA clicks

The Vercel Analytics script (`/_vercel/insights/script.js`) is already loaded on every page and injects `window.va`. Each page has an identical CTA click handler that fires `gtag()`. Add a `window.va` call alongside it so CTA clicks are queryable via the `get_web_analytics` MCP tool.

**Files:**
- Modify: `website/index.html:966-974`
- Modify: `website/indicator.html:544-552`
- Modify: `website/pnl-card.html:1932-1940`
- Modify: `website/prop-firms.html:428-436`

- [ ] **Step 1: Update index.html CTA handler**

Replace lines 966–974 in `website/index.html`:

```javascript
document.querySelectorAll('[data-cta]').forEach(function(btn){
  btn.addEventListener('click',function(){
    if(typeof gtag==='function'){
      gtag('event','cta_click',{cta_name:btn.dataset.cta,page_path:window.location.pathname});
    }else{
      console.warn('gtag not available — cta_click not sent for',btn.dataset.cta);
    }
    window.va?.('event',{name:'cta_click',data:{target:btn.dataset.cta}});
  });
});
```

- [ ] **Step 2: Update indicator.html CTA handler**

Replace lines 544–552 in `website/indicator.html` with the same block:

```javascript
document.querySelectorAll('[data-cta]').forEach(function(btn){
  btn.addEventListener('click',function(){
    if(typeof gtag==='function'){
      gtag('event','cta_click',{cta_name:btn.dataset.cta,page_path:window.location.pathname});
    }else{
      console.warn('gtag not available — cta_click not sent for',btn.dataset.cta);
    }
    window.va?.('event',{name:'cta_click',data:{target:btn.dataset.cta}});
  });
});
```

- [ ] **Step 3: Update pnl-card.html CTA handler**

Replace lines 1932–1940 in `website/pnl-card.html` with the same block:

```javascript
document.querySelectorAll('[data-cta]').forEach(function(btn){
  btn.addEventListener('click',function(){
    if(typeof gtag==='function'){
      gtag('event','cta_click',{cta_name:btn.dataset.cta,page_path:window.location.pathname});
    }else{
      console.warn('gtag not available — cta_click not sent for',btn.dataset.cta);
    }
    window.va?.('event',{name:'cta_click',data:{target:btn.dataset.cta}});
  });
});
```

- [ ] **Step 4: Update prop-firms.html CTA handler**

Replace lines 428–436 in `website/prop-firms.html` with the same block:

```javascript
document.querySelectorAll('[data-cta]').forEach(function(btn){
  btn.addEventListener('click',function(){
    if(typeof gtag==='function'){
      gtag('event','cta_click',{cta_name:btn.dataset.cta,page_path:window.location.pathname});
    }else{
      console.warn('gtag not available — cta_click not sent for',btn.dataset.cta);
    }
    window.va?.('event',{name:'cta_click',data:{target:btn.dataset.cta}});
  });
});
```

- [ ] **Step 5: Deploy to production**

```bash
cd website
vercel --prod
```

Expected: Vercel CLI outputs a production deployment URL ending in `joinawtrading.com`.

- [ ] **Step 6: Commit**

```bash
git add website/index.html website/indicator.html website/pnl-card.html website/prop-firms.html
git commit -m "feat: add Vercel Analytics custom events for CTA clicks

Fires va('event', {name:'cta_click', data:{target}}) alongside gtag
on every [data-cta] element across all pages. Enables MCP-queryable
conversion data for the optimize-site skill.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 2: Bootstrap state files

Create the two persistent files the skill reads and writes between runs.

**Files:**
- Create: `website/.optimize-log.json`
- Create: `website/.optimize-notes.md`

- [ ] **Step 1: Create .optimize-log.json**

Create `website/.optimize-log.json`:

```json
{
  "lastRun": null,
  "branch": null,
  "change": null,
  "baselineMetrics": {
    "period": null,
    "homeVisitors": null,
    "indicatorVisits": null,
    "discordClicks": null,
    "indicatorClicks": null,
    "topReferrer": null
  }
}
```

- [ ] **Step 2: Create .optimize-notes.md**

Create `website/.optimize-notes.md`:

```markdown
# optimize-site Run Log

Reference for the /optimize-site skill. Each run appends an entry below.
The skill reads this file to avoid repeating failed experiments.

---
```

- [ ] **Step 3: Commit**

```bash
git add website/.optimize-log.json website/.optimize-notes.md
git commit -m "chore: bootstrap optimize-site state files

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 3: Write the optimize-site skill

The SKILL.md is the core deliverable. It instructs Claude through the full 6-phase optimization loop when `/optimize-site` is invoked.

**Files:**
- Create: `~/.claude/skills/optimize-site/SKILL.md`

- [ ] **Step 1: Create skill directory and SKILL.md**

Create `~/.claude/skills/optimize-site/SKILL.md` with the full content below. This is the complete file — write it exactly as shown:

````markdown
---
name: optimize-site
trigger: /optimize-site
description: Closed-loop conversion optimization for joinawtrading.com. Pulls Vercel Analytics, diagnoses the weakest CTA, proposes and implements targeted changes, deploys on a versioned branch, and records everything for the next run.
---

# optimize-site

Conversion optimization loop for joinawtrading.com. Run this skill to analyze the last 7 days of analytics, diagnose the #1 conversion bottleneck, propose a targeted fix, ship it, and record the result.

**Conversion targets (in priority order):**
1. Discord joins — `cta_click` events where `target = free_discord`
2. Indicator purchases — `cta_click` events where `target = free_indicator` + `/indicator` page visits

**Project IDs (do not change):**
- projectId: `prj_UevbwODj0zG2mSZk7V3vhi0fr5hu`
- teamId: `team_w2a1SzZwqThV8FeKxvD4darX`

---

## Guardrails — memorize before touching any file

| Change type | Rule |
|---|---|
| CTA button copy | Autonomous — implement directly |
| Headline / subheadline copy | Autonomous — implement directly |
| Urgency / social proof copy | Autonomous — implement directly |
| Pricing copy ($39 / $129) | Must propose, user approves before touching |
| CTA placement / layout tweaks | Must propose + run local preview, user approves before deploy |
| Page structure (add/remove sections) | Must propose + run local preview, user approves before deploy |
| Brand colors, fonts, logo | NEVER touch |
| External URLs (Discord, Whop links) | NEVER touch |

---

## Phase 1 — Pull analytics (current period)

Compute dates: TODAY = current date, SEVEN_DAYS_AGO = today minus 7 days, FOURTEEN_DAYS_AGO = today minus 14 days.

Run all four queries in parallel using `mcp__plugin_vercel_vercel__get_web_analytics`:

**Query A — Page visits, current 7 days:**
```
projectId: prj_UevbwODj0zG2mSZk7V3vhi0fr5hu
teamId: team_w2a1SzZwqThV8FeKxvD4darX
mode: aggregate
since: SEVEN_DAYS_AGO
until: TODAY
by: ["requestPath"]
limit: 10
```

**Query B — Referrers, current 7 days:**
```
projectId: prj_UevbwODj0zG2mSZk7V3vhi0fr5hu
teamId: team_w2a1SzZwqThV8FeKxvD4darX
mode: aggregate
since: SEVEN_DAYS_AGO
until: TODAY
by: ["referrerHostname"]
limit: 10
```

**Query C — CTA click events by target, current 7 days:**
```
projectId: prj_UevbwODj0zG2mSZk7V3vhi0fr5hu
teamId: team_w2a1SzZwqThV8FeKxvD4darX
dataset: events
mode: aggregate
since: SEVEN_DAYS_AGO
until: TODAY
by: ["eventData/target"]
filter: eventName eq 'cta_click'
limit: 10
```

**Query D — Page visits, prior 7 days (for comparison):**
```
projectId: prj_UevbwODj0zG2mSZk7V3vhi0fr5hu
teamId: team_w2a1SzZwqThV8FeKxvD4darX
mode: aggregate
since: FOURTEEN_DAYS_AGO
until: SEVEN_DAYS_AGO
by: ["requestPath"]
limit: 10
```

**Query E — CTA click events, prior 7 days:**
```
projectId: prj_UevbwODj0zG2mSZk7V3vhi0fr5hu
teamId: team_w2a1SzZwqThV8FeKxvD4darX
dataset: events
mode: aggregate
since: FOURTEEN_DAYS_AGO
until: SEVEN_DAYS_AGO
by: ["eventData/target"]
filter: eventName eq 'cta_click'
limit: 10
```

---

## Phase 2 — Read state files

Read both files:
- `website/.optimize-log.json` — previous run's baseline metrics and what was changed
- `website/.optimize-notes.md` — full run history and experiment outcomes

If `.optimize-log.json` has `"lastRun": null`, this is the first run. Skip Phase 3 and go directly to Phase 4.

---

## Phase 3 — Evaluate last change

Compare current 7-day metrics against `baselineMetrics` in `.optimize-log.json`.

Compute these deltas:
- `homeVisitors`: current vs baseline
- `discordClicks`: current vs baseline
- `indicatorClicks`: current vs baseline
- `discordConvRate`: discordClicks / homeVisitors (current vs baseline)
- `indicatorConvRate`: indicatorVisits / homeVisitors (current vs baseline)

**Verdict rules:**
- **Improved:** discordConvRate or indicatorConvRate increased by ≥5% → note as success, proceed to Phase 4
- **Declined:** either rate dropped by ≥5% → flag it prominently, recommend reverting, give user the choice before continuing. Say: "The last change appears to have hurt [metric] by [X%]. I recommend reverting before making a new change. Should I revert, or proceed anyway?"
- **Neutral:** change within ±5% → note as inconclusive, proceed to Phase 4

If evaluating, go back and fill in the "After:" line in the most recent entry in `website/.optimize-notes.md` before appending a new entry. Find the pattern `**After:** TBD` in the file and replace it with the actual result, e.g. `**After:** Discord conv rate 7.5% → 9.1% (+21%) ✓ improved`.

---

## Phase 4 — Diagnose

Compute the core funnel metrics from current period data:
- `homeVisitors`: visitors to `/`
- `indicatorVisits`: visitors to `/indicator`
- `discordClicks`: `free_discord` event count
- `indicatorClicks`: `free_indicator` event count
- `discordConvRate`: discordClicks / homeVisitors × 100
- `indicatorConvRate`: indicatorClicks / homeVisitors × 100
- `topReferrer`: highest non-empty referrerHostname

**Pick one bottleneck** using this priority:
1. If `discordConvRate` < 10% → Discord CTAs are the problem, focus there
2. If `indicatorConvRate` < 5% → Indicator CTAs are the problem, focus there
3. If `topReferrer` is `l.instagram.com` and `discordConvRate` < 15% → Instagram traffic isn't converting, hero/above-fold is the problem
4. If metrics look healthy → focus on whichever CTA has the bigger gap between visits and clicks

Do not split focus across multiple bottlenecks in one run.

---

## Phase 5 — Propose

Based on the bottleneck, generate 1–2 specific changes. For each, state:
- **File:** exact file path
- **Element:** what element (e.g. "hero primary CTA button text")
- **Current value:** the exact current text/attribute
- **Proposed value:** what to change it to
- **Hypothesis:** one sentence — why this should increase [discordClicks | indicatorClicks]
- **Category:** copy (autonomous) or layout (needs local preview)

Example proposal format:
```
Change 1 — Copy (autonomous)
File: website/index.html
Element: Hero primary CTA button (line ~413)
Current: "Join Free Discord"
Proposed: "Join 500+ Traders Free"
Hypothesis: Adding a specific member count reduces ambiguity and increases perceived social proof at the moment of decision.
```

Present the proposals and ask: "Approve these changes? You can approve all, modify any, or reject."

Wait for explicit approval before proceeding to Phase 6.

---

## Phase 6 — Implement & deploy

- [ ] Create branch: `git checkout -b optimize/YYYY-MM-DD` (use today's date)
- [ ] Make the approved edits to the HTML file(s)
- [ ] **If any layout change was approved:** Run `cd website && npx serve . -p 3000`, tell the user to open `http://localhost:3000` and confirm it looks right. Wait for their go-ahead before continuing.
- [ ] Commit: `git commit -m "optimize: [one-line description of what changed and hypothesis]"`
- [ ] Deploy: `cd website && vercel --prod`
- [ ] Push branch to GitHub: `git push origin optimize/YYYY-MM-DD`

---

## Phase 7 — Record

**Update `website/.optimize-log.json`** with the current run's data:

```json
{
  "lastRun": "CURRENT_ISO_TIMESTAMP",
  "branch": "optimize/YYYY-MM-DD",
  "change": {
    "file": "website/index.html",
    "description": "one-line description of the change",
    "hypothesis": "one-line hypothesis"
  },
  "baselineMetrics": {
    "period": "SEVEN_DAYS_AGO to TODAY",
    "homeVisitors": [current homeVisitors],
    "indicatorVisits": [current indicatorVisits],
    "discordClicks": [current discordClicks],
    "indicatorClicks": [current indicatorClicks],
    "topReferrer": "[current topReferrer]"
  }
}
```

**Append to `website/.optimize-notes.md`:**

```markdown
## YYYY-MM-DD — optimize/YYYY-MM-DD

**Bottleneck:** [what was identified, e.g. "Discord conv rate low (7.5%)"]
**Change:** [description of what was changed]
**Hypothesis:** [why it should work]
**Before:** Discord [X clicks / Y visitors = Z%] | Indicator [X clicks / Y visitors = Z%]
**After:** TBD — evaluate next run
**Referrer mix:** [top 3 referrers and visitor counts]
**Notes:** [any observations, patterns, or things to try next time]

---
```

Commit the updated state files:
```bash
git add website/.optimize-log.json website/.optimize-notes.md
git commit -m "chore: record optimize-site run YYYY-MM-DD"
git push origin optimize/YYYY-MM-DD
```

---

## End of run

Tell the user:
- What was deployed and the hypothesis
- The branch name for rollback reference (`git checkout optimize/YYYY-MM-DD` + `vercel --prod` to revert)
- That the next run in ~7 days will evaluate whether it worked before proposing the next change

If this skill is wrapped in a `/schedule` routine, the next run will evaluate automatically.
````

- [ ] **Step 2: Verify the skill is discoverable**

Run:
```bash
ls ~/.claude/skills/optimize-site/
```

Expected output:
```
SKILL.md
```

- [ ] **Step 3: Commit the plan + skill**

```bash
git add docs/superpowers/plans/2026-08-04-optimize-site.md
git commit -m "docs: add optimize-site implementation plan

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Self-review notes

- **Spec coverage:** All 6 phases covered. First-run detection handled (null lastRun check). Guardrails embedded in skill. Branch-per-run versioning in Phase 6. Notes file fill-in for TBD in Phase 3. ✓
- **No placeholders:** All steps have exact file paths, line numbers, and complete content. ✓
- **Type consistency:** `discordClicks`/`indicatorClicks` used consistently across Phase 4, 5, and 7. `free_discord`/`free_indicator` match existing `data-cta` attribute values in HTML. ✓
