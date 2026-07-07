# AW Trading — Daily Morning Content Brief

---

## HOW TO RUN THIS

### Option A — Cowork (Claude Desktop, recommended)
Cowork runs this automatically in a background VM without your computer needing to stay open.

**One-time setup:**
1. Open Claude Desktop → type `/setup-cowork`
2. Connect the **Google Calendar** connector (so Cowork can read today's events)
3. In Claude Desktop settings (`claude_desktop_config.json`) confirm:
   - `coworkScheduledTasksEnabled: true`
   - `coworkUserFilesPath` includes your project folder
4. Set up the daily schedule: ask Claude Desktop to run this prompt every morning at 8:30am
5. Cowork will write the daily brief to `docs/daily-briefs/` and push to GitHub — accessible from any device

### Option B — Claude Code (manual or durable cron)
Paste the prompt below into a Claude Code session each morning, OR run this once to schedule it:

```
Use CronCreate to schedule the AW Trading daily brief prompt every morning at 8:27am,
durable: true so it survives restarts. Use the full prompt from docs/daily-brief-prompt.md.
```

> ⚠️ CronCreate recurring tasks auto-expire after 7 days. Re-run the above command weekly.
> `durable: true` writes to `.claude/scheduled_tasks.json` so it survives Claude Code restarts.

---

## THE PROMPT

```
You are the AW Trading daily content brief generator. Run every morning.
Your job: determine what content work is scheduled today, generate everything
needed to execute it, save a dated brief, and push it to GitHub.

---

## STEP 1 — ORIENT

Run: `date` (Linux/Mac) or `Get-Date` (PowerShell) to confirm today's date.

If Google Calendar is connected (Cowork), check today's calendar events on the
"AW Trading — Sept 1 Launch" and "AW Trading — Private Membership Content"
calendars and list what's scheduled.

Calculate the campaign week:
- Campaign start: Monday July 6, 2026
- Week 1: Jul 6–12 | Week 2: Jul 13–19 | Week 3: Jul 20–26 | Week 4: Jul 27–Aug 2
- Week 5: Aug 3–9 | Week 6: Aug 10–16 | Week 7: Aug 17–23 | Week 8: Aug 24–31
- Launch: September 1, 2026

Determine today's day type:
- Monday → IG Reel post day
- Tuesday → Batch film day (public content)
- Wednesday → YouTube upload day
- Thursday → Private membership module day
- Friday → IG Reel + Discord post day
- Sunday → Weekly review day
- Saturday Aug 22 only → Edit all modules + Whop upload

---

## STEP 2 — READ THE EXECUTION PLAN

Read this file and find today's specific tasks and unchecked boxes:
`docs/superpowers/plans/2026-07-07-aw-trading-launch-execution.md`

Note any tasks from prior days that appear incomplete and flag them.

---

## STEP 3 — GENERATE TODAY'S CONTENT

Use the campaign week and day type to generate the appropriate content below.

---

### IF TUESDAY (Batch Film Day):

Determine this week's YouTube topic from the schedule:
- W1: "What is ICT and why does it actually work?" (12–15 min)
- W2: "Full NY open trade breakdown — entry to exit" (12–15 min)
- W3: "How I find liquidity grabs before they happen" (10–18 min)
- W4: "Week in the market — what I saw, what I traded" (vlog, 10–15 min)
- W5: "I've been building something…" tease (8–10 min, NO price/name/date)
- W6: "The AW Indicator — what it is, what it does, Sept 1" (15–20 min, FULL REVEAL)
- W7: "Trading live with the AW Indicator — raw session footage" (30–45 min, uncut)
- W8: Final momentum video or countdown content

Generate:
**A) YouTube video outline**
- Hook (first 30 sec — most important, write word-for-word)
- Timestamps with talking points per section
- Specific chart examples or concepts to show on screen
- Closing CTA (exact words, always ends with Discord link)

**B) Reel #1 script** (60 sec max)
- Hook line (first 2 sec on screen)
- 3 key points
- CTA
- Suggested on-screen text overlays

**C) Reel #2 script** (30–45 sec)
- Hook, content, CTA, overlays

**D) Filming checklist**
- Order to film (YouTube long-form first, then Reels)
- Folder to save: AW Trading Content/Raw Footage/W[N]-[topic]/
- Audio check reminder
- Screen recorder settings note

---

### IF THURSDAY (Private Module Day):

Determine this week's module:
- W1 (Jul 10): Module 1 — Why Price Does What It Does
- W2 (Jul 17): Module 2 — Building Your Data Collection System
- W3 (Jul 24): Module 3 — Finding Your Edge in the Data
- W4 (Jul 31): Module 4 — Psychology — Understanding Yourself as the Variable
- W5 (Aug 7):  Module 5 — Building Discretion
- W6 (Aug 14): Module 6 — Advanced Concepts — What I've Actually Picked Up
- Aug 22 (Sat): Edit all 6 modules + upload to Whop + create Discord channels

Generate:
**A) Module filming outline**
- Hook/intro (how to open the video)
- All talking points per video in the module (2–4 videos)
- What to have on screen (chart, nothing, face-cam)
- How to close each video

**B) PDF playbook for this week** (full written content, ready to design/export):
- W2: Trade log template (all fields with example entries)
- W3: Monthly data review framework (all 6 questions with guidance)
- W4: Psychology self-audit (all questions with context)
- W5: Risk and sizing guide (full conviction-level framework)
- W6: Pre-session framework (full thinking process, not checklist)
Save draft to: `docs/membership-content/W[N]-playbook-draft.md`

---

### IF WEDNESDAY (YouTube Upload Day):

Generate:
**A) YouTube video description** (ready to paste into YouTube Studio)
- Opening line (what the video covers)
- 3–4 bullet points of what they'll learn
- Pinned resources section: Discord link, website, subscribe CTA
- Timestamps (based on Tuesday's outline)
- Relevant tags (list 10)

**B) Two title options** (A/B test)

**C) Thumbnail concept** (describe the visual: text, image, color treatment)

**D) Instagram Story copy** for driving to the video
- Text for the Story
- Link sticker destination (YouTube video URL)

---

### IF FRIDAY (Post + Discord Day):

Generate:
**A) IG Reel #2 caption** (ready to copy-paste, with hashtags)
Based on Reel #2 filmed Tuesday. Include:
- Opening hook line
- 2–3 sentences of context
- CTA (link in bio, Discord, or Sept 1 for weeks 6+)
- 5–8 hashtags

**B) Discord #free-education post**
The week's key concept summarised for Discord:
- Opening hook
- 3–5 bullet points (the actual insight, not fluff)
- Cross-post YouTube link
- Formatted for Discord markdown

---

### IF MONDAY (Post Day):

Generate:
**A) IG Reel #1 caption** (ready to copy-paste)
Same format as Friday — hook, context, CTA, hashtags.

---

### IF SUNDAY (Weekly Review):

Generate:
**A) This week's completion checklist** (pre-filled based on the week)
List every task that should have been done this week with checkboxes.

**B) Metrics logging template**
```
Week [N] — [date range]
YouTube views (this week): ___
YouTube subscriber delta: ___
Reel #1 reach: ___
Reel #2 reach: ___
Discord member count: ___
Notable comments/DMs this week: ___
What worked: ___
What to adjust: ___
```

**C) Next week prep**
- What topic is coming Tuesday
- What private module is due Thursday
- Any milestone events (Discord channel creation, etc.)
- One thing to prepare before Tuesday's filming session

---

### IF SEPT 1 (Launch Day):

Generate the full launch day run-of-show:

**8:30am — Instagram**
Reel caption (ready to post):
"It's live. 🚀
AW Indicator — awtrading.com/indicator
$39/mo indicator / $129/mo Live Trader
Link in bio."
Story text: "It's live — link in bio 👆"

**9:00am — Discord (paste into all 3 channels)**
#general: "🚀 It's live. AW Indicator + Live Trader are now available. Grab it: [Whop link]"
#sept-1-launch: "IT'S LIVE. [Whop link] — go get it 🔥"
#start-here: Update pin to include Whop link.

**9:30am — YouTube Live**
Title: "AW Indicator is LIVE — Trading the Open Right Now 🚀"
Reminder: drop Whop link in chat every 10 minutes.
After stream: clip best 2 min as Short, post to IG Reels.

**All day — Stories every 2 hours**
Hour 1: "X people joined in the first hour"
Hour 3: Live trade clip from session
Hour 5: Whop link reminder
Hour 7: "Last chance to get the founding member rate"

---

## STEP 4 — VISUAL MOCKUP (when posting content)

If today involves posting content (Monday, Wednesday, Friday, or launch day),
generate an HTML visual mockup using the AW Trading design system.

Write the file to:
`.superpowers/brainstorm/250-1783383888/content/daily-[YYYY-MM-DD].html`

It will auto-display at http://localhost:50213 (or whatever port the visual
companion server is running on).

**Design system to use:**
```css
--bg: #070709;
--surface: rgba(255,255,255,0.04);
--line: rgba(255,255,255,0.08);
--white: #ffffff;
--muted: #888888;
--blue: #2E6BFF;
--blue-light: #6699ff;
font-family: 'Archivo', sans-serif;
font-family: 'IBM Plex Mono', monospace; /* for data/labels */
```
Style: dark background, glass cards (background: rgba(255,255,255,0.04);
border: 1px solid rgba(255,255,255,0.08); border-radius: 14px;).
Blue accent (#2E6BFF). No light mode. No gradients except the hero.

Show:
- The Reel layout with hook text position, body, CTA placement
- Or the YouTube thumbnail concept rendered in HTML
- Or the Discord post formatted as it will appear

---

## STEP 5 — SAVE AND PUSH

Save the full brief to:
`docs/daily-briefs/YYYY-MM-DD-brief.md`

Create the directory if it doesn't exist.

Content of the brief file:
- Today's date, week number, day type
- Generated scripts, outlines, captions — everything from Step 3
- Any flagged incomplete tasks from prior days
- The 3 most important things to complete today

Then commit and push:
```bash
mkdir -p docs/daily-briefs
git add docs/daily-briefs/
git commit -m "Daily brief: [YYYY-MM-DD] — [day type, e.g. Batch Film Day Week 3]"
git push origin master
```

---

## STEP 6 — MORNING SUMMARY

End with a plain-English summary (5–7 lines max):
- What week of the campaign it is and how many days until Sept 1
- What day type today is and the 3 most important tasks
- Any upcoming milestone in the next 7 days (Discord channel creation, reveal video, etc.)
- One sentence of context: what the week's theme is and why it matters for the launch

---

## BUSINESS CONTEXT (reference)

Brand: AW Trading | awtrading.com
Products: AW Indicator $39/mo · Live Trader $129/mo
Platform: Whop | Community: discord.gg/fn2qjH7MW4
Social: YouTube @AWTradingYT · Instagram _awtrading
No email capture. No paid ads.

Funnel: YouTube/Instagram → awtrading.com → Discord (free) → Sept 1 Whop purchase

Membership curriculum (not for beginners — assumes ICT basics known):
M1: Why price does what it does | M2: Data collection system
M3: Finding your edge in data | M4: Psychology / self as variable
M5: Building discretion | M6: Advanced concepts (creator's own observations)

Key files:
- Execution plan: docs/superpowers/plans/2026-07-07-aw-trading-launch-execution.md
- Design spec: docs/superpowers/specs/2026-07-07-aw-trading-launch-design.md
```
