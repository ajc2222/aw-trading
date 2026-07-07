# AW Trading Sept 1 Launch — Execution Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Execute the 8-week content and community nurture system to convert free Discord members into paying AW Indicator and Live Trader subscribers by September 1, 2026.

**Architecture:** Solo creator workflow — batch film public content Tuesdays, upload/post Wednesday–Friday, Discord education drops Friday, Sunday review. Thursday (1 hr) is private membership content filming. Weeks 1–4 are pure value. Weeks 5–7 shift to tease → announce → heat. Sept 1 is an all-platform simultaneous launch.

**Weekly rhythm:**
- Tuesday (2hr): batch film all public content for the week
- Thursday (1hr): film one private membership module + write one playbook
- Wednesday–Friday: post public content, Discord education drop
- Sunday: metrics review + next week prep

**Tech Stack:** YouTube Studio, Instagram (Reels + Stories), Discord, Whop, awtrading.com (Vercel), screen recorder (OBS or built-in), video editor (CapCut, DaVinci, or Premiere)

---

## Pre-Launch Setup (Complete Before Week 1)

### Task 0: Environment and accounts check

**Files:**
- Verify: `docs/superpowers/specs/2026-07-07-aw-trading-launch-design.md`
- Website live at: `awtrading.com` (Vercel, already deployed)

- [ ] **Step 1: Confirm website is live with countdown**

  Open `awtrading.com` in a browser. Verify:
  - Countdown bar visible below nav
  - YouTube and Instagram icons in nav (desktop) and footer
  - All 4 main pages have the countdown

- [ ] **Step 2: Confirm social profiles are linked in bio**

  Instagram bio link → `awtrading.com`
  YouTube channel description → `awtrading.com` + Discord link
  If either is missing, update now.

- [ ] **Step 3: Import Google Calendar file**

  Open `docs/aw-trading-launch-calendar.ics` → drag into Google Calendar.
  Verify "AW Trading — Sept 1 Launch" calendar appears with events through Sept 1.

- [ ] **Step 4: Set up screen recorder**

  Install or confirm OBS / QuickTime / built-in recorder is working.
  Do a 30-second test recording of your chart platform. Confirm audio is clean.

- [ ] **Step 5: Create a "Content Vault" folder**

  Create a local folder: `AW Trading Content/`
  Subfolders:
  ```
  AW Trading Content/
    Raw Footage/
    Edited/
      YouTube/
      Reels/
    Posted/
    Assets/
      P&L Screenshots/
      Certifications/
      Chart Annotations/
  ```

- [ ] **Step 6: Confirm Whop account is set up**

  Log into Whop. Confirm you can publish products on Sept 1.
  Indicator product page should be drafted (unpublished) with:
  - $39/mo price
  - Description, screenshots, Discord access
  Do NOT publish yet.

- [ ] **Step 7: Commit setup complete**

  ```bash
  git add docs/
  git commit -m "Launch execution plan added"
  git push origin master
  ```

---

## Task 1: Week 1 — Establish Authority (Jul 6–12)

**Theme:** Pure free value. No pitch. Build trust from day one.

**Files:**
- Post to: YouTube, Instagram
- Discord: `#free-education`

### Tuesday Jul 7 — Batch Film Day

- [ ] **Step 1: Draft YouTube outline**

  Video: "What is ICT and why does it actually work?"
  Outline:
  ```
  0:00  Hook — "Most traders lose because they trade against the wrong people"
  0:45  What ICT is (institutional order flow, not retail indicators)
  3:00  Concept 1: Market structure
  6:00  Concept 2: Liquidity (buy-side / sell-side)
  9:00  Concept 3: Order blocks
  12:00 How these three combine on a real chart (annotated example)
  14:00 CTA — "Free community in description, I post these breakdowns daily"
  ```

- [ ] **Step 2: Film YouTube video**

  Target: 12–15 minutes. Record with chart visible.
  Don't restart on mistakes — keep filming, edit out later. One take is fine.
  Save to `Raw Footage/W1-youtube-ict-breakdown.mp4`

- [ ] **Step 3: Film Reel #1 — "3 ICT terms"**

  Script (60 sec):
  ```
  "3 ICT terms that will change how you read price — go.
  Number 1: Liquidity. Price hunts stop losses before reversing.
  Number 2: Order blocks. Institutional footprints left on the chart.
  Number 3: Market structure. Higher highs and higher lows — who's in control.
  Master these three and you'll never look at price the same way.
  Free breakdowns in my community — link in bio."
  ```
  Film portrait (9:16). Save to `Raw Footage/W1-reel1-ict-terms.mp4`

- [ ] **Step 4: Film Reel #2 — P&L + chart annotation**

  Pull a recent P&L screenshot from `Assets/P&L Screenshots/`.
  Screen record the chart with the trade annotated.
  Voiceover: "Here's what I saw before entry, and here's the result."
  30–45 seconds. Save to `Raw Footage/W1-reel2-pnl.mp4`

- [ ] **Step 5: Edit all three**

  YouTube: trim dead air, add chapter markers. Export 1080p.
  Reels: add captions (auto-caption in CapCut or Instagram), add hook text overlay in first 2 seconds.
  Save edited files to `Edited/YouTube/` and `Edited/Reels/`

### Wednesday Jul 8 — Upload Day

- [ ] **Step 6: Post Reel #1 — "3 ICT terms"**

  Caption:
  ```
  ICT simplified 👇

  Liquidity — price hunts stops before reversing
  Order blocks — institutional footprints on the chart
  Market structure — who's actually in control

  Save this. Free community → link in bio

  #ICT #futurestrading #daytrading #priceaction #AWTrading
  ```

- [ ] **Step 7: Upload YouTube video**

  Title: `What is ICT Trading and Why Does It Actually Work?`
  Description:
  ```
  In this video I break down exactly what ICT trading is and why the concepts
  actually work — not theory, live charts.

  📌 Join the free community: discord.gg/fn2qjH7MW4
  🌐 awtrading.com
  🔔 Subscribe for weekly breakdowns

  Timestamps:
  0:00 Intro
  0:45 What ICT is
  3:00 Market structure
  6:00 Liquidity
  9:00 Order blocks
  12:00 Live chart example
  14:00 Free community
  ```
  Add to playlist "Free Education". Schedule for 9am or publish immediately.

- [ ] **Step 8: Post IG Story — audience poll**

  Story text: "Quick question 👇"
  Poll: "Do you trade sessions or all day?"
  Option A: Session trader | Option B: All day

### Friday Jul 10 — Second post day

- [ ] **Step 9: Post Reel #2 — P&L + chart**

  Caption:
  ```
  Here's what I saw before entry 📊

  [1-2 sentences: session, level, confirmation]

  Full breakdowns in the free community daily → link in bio

  #priceaction #futurestrading #ICT #tradingresults
  ```

- [ ] **Step 10: Post in Discord #free-education**

  Post the key concept from this week's YouTube video. Example:
  ```
  📚 Concept of the week: Liquidity

  Before price makes a significant move, it almost always raids liquidity first.
  - Buy-side liquidity = stops above swing highs
  - Sell-side liquidity = stops below swing lows

  Watch for the raid → reversal pattern on your chart this week.

  Full breakdown on YouTube → [link]
  ```

### Sunday Jul 12 — Weekly Review

- [ ] **Step 11: Log metrics**

  Open a notes app or spreadsheet. Log:
  ```
  Week 1 Metrics
  YouTube views: ___
  YouTube subscribers (delta): ___
  Reel #1 reach: ___
  Reel #2 reach: ___
  Discord members: ___
  ```

- [ ] **Step 12: Review checklist**

  ```
  ✅ YouTube video uploaded?
  ✅ 2 Instagram Reels posted?
  ✅ 1 Instagram Story posted?
  ✅ Discord #free-education post done?
  ✅ Comments and DMs replied to?
  ```

- [ ] **Step 13: Prep Week 2 topic**

  Identify a real trade from this week to use in the "NY open breakdown" video.
  Screenshot the chart entry. Save to `Assets/Chart Annotations/W2-trade.png`

---

## Task 2: Week 2 — Teach a System (Jul 13–19)

**Theme:** Real trade walkthrough. Session recap builds the most trust fastest.

### Tuesday Jul 15 — Batch Film Day

- [ ] **Step 1: Film YouTube — full trade breakdown**

  Video: "Full NY open trade breakdown — entry to exit"
  Structure:
  ```
  0:00  Hook — show the P&L first, then say "here's everything that happened"
  0:30  Pre-session prep (what levels were marked)
  3:00  Session open — what you saw
  6:00  Entry — why here, not earlier or later
  9:00  Management — how you held it
  11:00 Exit — how you knew it was done
  13:00 Lesson — one thing to take away
  14:00 Discord CTA
  ```
  Save to `Raw Footage/W2-youtube-trade-breakdown.mp4`

- [ ] **Step 2: Film YouTube Short — "Why most traders enter too early"**

  45 seconds. Pull a clip from the trade video where you show the early entry trap.
  Voiceover: "This is where most traders enter. Here's where I wait."
  Save to `Raw Footage/W2-short-early-entry.mp4`

- [ ] **Step 3: Film Reel #1 — A+ ICT setup annotation**

  Screen record the chart with annotation drawn live. 30–45 sec.
  Voiceover: "This is what an A+ entry looks like — [session], [level], [confirmation]."
  Save to `Raw Footage/W2-reel1-aplus-setup.mp4`

- [ ] **Step 4: Film Reel #2 — cert or prop pass**

  Screen record the prop firm dashboard showing the pass.
  Voiceover: brief explanation of the trade/week that got you there.
  30 seconds. Save to `Raw Footage/W2-reel2-proppass.mp4`

- [ ] **Step 5: Edit all content**

  YouTube: chapter markers, trim. Export 1080p.
  Short: vertical crop, captions. Under 60 sec.
  Reels: captions, hook text overlay.

### Wednesday Jul 16 — Upload Day

- [ ] **Step 6: Post Reel #1 — A+ setup**

  Caption:
  ```
  This is what an A+ entry looks like 📊

  [Session] — price swept [level] — confirmation at [structure point]

  I post setups like this in the free community daily → link in bio

  #ICTtrading #futurestrading #priceaction #daytrader
  ```

- [ ] **Step 7: Upload YouTube + Short**

  Title: `Full NY Open Trade Breakdown — Entry to Exit (Real Trade)`
  Description: same template as Week 1, updated for this trade.
  Upload Short separately: `Why Most Traders Enter Too Early`
  Both to "Free Education" playlist.

- [ ] **Step 8: Post IG Story — drive to YouTube**

  Use a still from the video or a chart screenshot.
  Text: "Full trade breakdown posted — entry to exit, no edits."
  Add link sticker → YouTube video URL.

### Friday Jul 18

- [ ] **Step 9: Post Reel #2 — prop pass**

  Caption:
  ```
  Passed another one 💰

  [Firm] — $[size] account

  The exact setups I used → free community in bio

  #propfirm #fundedtrader #futurestrading #tradingresults
  ```

- [ ] **Step 10: Discord #free-education post**

  Post a session recap from this week. 3–4 sentences + chart screenshot.

### Sunday Jul 19 — Weekly Review

- [ ] **Step 11: Log metrics** (same format as Week 1)
- [ ] **Step 12: Screenshot and save the Week 3 Q&A Story responses reminder**

  Note in your calendar or phone: "Week 3 — post Q&A sticker Story. Screenshot ALL responses."

---

## Task 3: Week 3 — Social Proof + Education (Jul 20–26)

**Theme:** Use real credentials. The Q&A Story this week is critical — save every response for Week 6.

### Tuesday Jul 22 — Batch Film Day

- [ ] **Step 1: Film YouTube — "How I find liquidity grabs before they happen"**

  Structure:
  ```
  0:00  Hook — "Price always tells you where it's going before it gets there"
  1:00  What a liquidity grab is (visual)
  3:00  How to identify BSL / SSL on your chart
  6:00  The 3-step checklist: structure → liquidity → confirmation
  10:00 Live chart: 2–3 examples
  15:00 Discord CTA
  ```
  Save to `Raw Footage/W3-youtube-liquidity-grabs.mp4`

- [ ] **Step 2: Film Reel #1 — "I passed a $50K prop eval using this one concept"**

  Pull the $50K cert from `Assets/Certifications/`.
  Screen record showing the cert + the concept on a chart.
  Voiceover: "Passed a $50K eval using [concept]. Here's what it looks like."
  Save to `Raw Footage/W3-reel1-propeval.mp4`

- [ ] **Step 3: Edit all content**

### Wednesday Jul 23

- [ ] **Step 4: Post Reel #1 — prop eval pass**

  Caption:
  ```
  Passed a $50K eval using this 👇

  [Concept name] — [1-2 sentence description]

  Free education → link in bio

  #propfirm #ICT #fundedtrader #futurestrading
  ```

- [ ] **Step 5: Upload YouTube video**

  Title: `How I Find Liquidity Grabs Before They Happen`

- [ ] **Step 6: Post IG Story — Q&A sticker (⚠️ SAVE EVERY RESPONSE)**

  Story text: "Be honest 👇"
  Add Q&A sticker: "Drop your biggest trading struggle"

  **After 24 hours:** screenshot every single response. Save to `Assets/QA-responses-w3.png`
  These become your Week 6 objection-flip Reel content. Do not skip this.

### Friday Jul 25

- [ ] **Step 7: Post Reel #2 — YouTube clip teaser**

  Pull the best 30-second clip from the YouTube video.
  Caption:
  ```
  Here's what a liquidity grab looks like in real time 👇

  Full breakdown on YouTube → link in bio

  #ICTtrading #priceaction #futurestrading
  ```

- [ ] **Step 8: Discord #free-education post**

  Post the 3-step liquidity checklist:
  ```
  📚 How I identify liquidity grabs — 3 steps:

  1. Mark HTF swing highs and lows (BSL/SSL)
  2. Watch for engineered moves into those levels during killzones
  3. Wait for displacement + lower timeframe confirmation before entry

  Full video on YouTube → [link]
  ```

### Sunday Jul 26 — Weekly Review

- [ ] **Step 9: Log metrics**
- [ ] **Step 10: Review Q&A responses**

  Read through all saved responses. Group them into 2–3 common themes.
  Write down the top objection — this becomes the Week 6 Reel script.
  Example themes: "I can't read the chart," "I keep getting stopped out," "I don't know when to enter"

---

## Task 4: Week 4 — Community + Live Value (Jul 27–Aug 2)

**Theme:** Show the Discord. Soft seed of "something coming." Make the community feel real.

### Tuesday Jul 29 — Batch Film Day

- [ ] **Step 1: Film YouTube — weekly market recap vlog**

  Lower production — phone or webcam, sit in front of your chart.
  Structure:
  ```
  0:00  "Here's what happened in the market this week"
  1:00  Monday: what you saw / traded
  4:00  Mid-week: key level that played
  8:00  Friday: how the week closed
  11:00 What to watch next week
  13:00 Discord CTA
  ```
  Save to `Raw Footage/W4-youtube-weekly-recap.mp4`

- [ ] **Step 2: Film YouTube Short — "2 seconds before a liquidity grab"**

  Find a live trade clip where you can show the 2 seconds right before price sweeps a level.
  Voiceover: "Watch this. 2 seconds before the grab. Most traders are already long here."
  Under 60 seconds. Save to `Raw Footage/W4-short-2sec-grab.mp4`

- [ ] **Step 3: Film Reel #1 — Discord server screen recording**

  Screen record a 30-second tour of the Discord: channels sidebar visible, scroll through #free-education, show #trade-breakdowns.
  Voiceover: "This is what's inside the free AW Trading community."
  Add a join CTA at the end. Save to `Raw Footage/W4-reel1-discord-tour.mp4`

- [ ] **Step 4: Film Reel #2 — trading mistake**

  Relatable mistake you made early on. Chart example if possible.
  Voiceover: "I used to do this — it cost me [outcome]. Here's what changed."
  30–45 sec. Save to `Raw Footage/W4-reel2-mistake.mp4`

- [ ] **Step 5: Edit all content**

### Wednesday Jul 30

- [ ] **Step 6: Post Reel #1 — Discord server tour**

  Caption:
  ```
  Free community for serious traders 👇

  Education, trade setups, live breakdowns — all free.

  Join → link in bio

  #trading #discordserver #futurestrading #ICTtrading
  ```

- [ ] **Step 7: Upload YouTube vlog + Short**

- [ ] **Step 8: Post IG Story — soft tease**

  No chart. Just text:
  "We're about 4 weeks from something I've been working on for a while 👀"
  Add a fire emoji. Nothing else.

### Friday Aug 1

- [ ] **Step 9: Post Reel #2 — trading mistake**

  Caption:
  ```
  Stop doing this if you want consistent results 🚫

  [Describe the mistake in 2 sentences]

  What fixed it for me → free community in bio

  #tradingtips #futurestrading #ICT #priceaction
  ```

- [ ] **Step 10: Discord #free-education post**

  Post market structure recap from this week. 3–4 bullet points + chart.

### Sunday Aug 2 — Weekly Review + Pre-Week-5 Checklist

- [ ] **Step 11: Log metrics**

- [ ] **Step 12: Pre-tease checklist**

  ```
  ⬜ #indicator-preview Discord channel — CREATE MONDAY AUG 3
  ⬜ Have 3 indicator clips ready for Week 5 (screen recordings of the indicator on chart)
  ⬜ Indicator displaying correctly on live chart — test before filming
  ```

---

## Task 5: Week 5 — First Tease (Aug 3–9)

**Theme:** Pure curiosity. No price. No name. Let the indicator speak through mystery.

### Monday Aug 3 — Discord Channel

- [ ] **Step 1: Create #indicator-preview channel**

  In Discord: Server Settings → Channels → New Channel → `indicator-preview`
  Set it below `#trade-breakdowns` in the channel list.

  First post in the channel:
  ```
  Something I've been building is almost ready.

  This channel is where you'll see it first. 👀
  ```

### Tuesday Aug 5 — Batch Film Day

- [ ] **Step 2: Film YouTube tease video**

  Video: "I've been building something for the past few months…"
  Structure:
  ```
  0:00  Hook — "I've been sitting on something for a while. Here it is."
  0:30  10–15 sec screen recording of indicator auto-drawing levels on live chart
  1:00  Cut — pivot to normal trading content (session recap or concept)
  8:00  End — "If you want to be the first to see this, Discord link below."
  ```
  Do NOT say the name, price, or date. Save to `Raw Footage/W5-youtube-tease.mp4`

- [ ] **Step 3: Film Reel #1 — indicator mystery clip**

  20-second screen recording. Indicator auto-draws levels. No voiceover.
  On-screen text: "what is this 👀"
  That's it. No explanation. Save to `Raw Footage/W5-reel1-mystery.mp4`

- [ ] **Step 4: Film Reel #2 — signal + result**

  Show the indicator signal firing on chart → outcome (P&L or price movement).
  30 sec. Voiceover: "Signal fired at [time]. Here's what happened."
  Save to `Raw Footage/W5-reel2-signal.mp4`

- [ ] **Step 5: Edit all content**

### Monday Aug 3

- [ ] **Step 6: Post Reel #1 — mystery clip**

  Caption:
  ```
  what is this 👀
  ```
  Pin the best comment if someone guesses correctly.

### Wednesday Aug 6

- [ ] **Step 7: Upload YouTube tease video**

  Title: `I've Been Working on Something…`
  Thumbnail: indicator on chart, face reaction.
  End screen: Discord link.

- [ ] **Step 8: Post IG Story**

  Screenshot of #indicator-preview channel in Discord.
  Text overlay: "Discord members find out first → link in bio 👇"

### Friday Aug 8

- [ ] **Step 9: Post Reel #2 — signal + result**

  Caption:
  ```
  Signal fired at [time]. Here's what happened 📈

  [2 sentence outcome]

  Want to see the tool? Discord members get first access → link in bio

  #trading #futurestrading #ICT
  ```

- [ ] **Step 10: Post 3rd teaser clip in Discord #indicator-preview**

  Post a third clip (different angle — levels, signal, or liquidity zone auto-draw).
  Caption:
  ```
  One more before the full reveal…

  The announcement is coming next week. 👀
  ```

### Sunday Aug 9 — Weekly Review + Pre-Announce Checklist

- [ ] **Step 11: Log metrics** (pay close attention to Reel comments on mystery clip)

- [ ] **Step 12: Pre-announce checklist**

  ```
  ⬜ Create #sept-1-launch Discord channel — MONDAY AUG 10
  ⬜ Create #testimonials Discord channel — MONDAY AUG 10
  ⬜ Confirm Whop product page is drafted and ready to link
  ⬜ Full reveal video filmed and edited (film this week if not done)
  ⬜ Review Week 3 Q&A responses — write the objection-flip Reel script
  ```

---

## Task 6: Week 6 — Announce (Aug 10–16)

**Theme:** First hard CTA. 6 weeks of trust earned this. Land it cleanly.

### Monday Aug 10 — Discord Channels

- [ ] **Step 1: Create #sept-1-launch channel**

  Pin the announcement post immediately:
  ```
  🚀 AW Indicator is launching September 1, 2026.

  $39/mo — full indicator access
  $129/mo — indicator + Live Trader mentorship

  [Whop link]

  Discord members get access the moment it goes live.
  ```

- [ ] **Step 2: Create #testimonials channel**

  Pin your best assets immediately:
  - Best P&L screenshot
  - Best certification
  - Best prop firm pass

  Post caption: "This is what's possible. Posting more as we approach launch."

### Tuesday Aug 12 — Batch Film Day

- [ ] **Step 3: Film YouTube — full reveal (⚠️ most important video)**

  Title: "The AW Indicator — What It Is, What It Does, and When It Launches"
  Structure:
  ```
  0:00  Hook — "I've been teasing this for weeks. Here's everything."
  0:30  Show the indicator live on chart — auto-draw walkthrough
  3:00  Feature 1: Session levels auto-drawing
  6:00  Feature 2: Liquidity zones
  9:00  Feature 3: A+ signal detection
  12:00 How I use it in a real session (clip)
  15:00 Launch date: September 1, 2026
  15:30 Pricing: $39/mo indicator / $129/mo Live Trader
  16:00 Where to get it: awtrading.com/indicator
  17:00 Discord early access framing + CTA
  ```
  Save to `Raw Footage/W6-youtube-reveal.mp4`

- [ ] **Step 4: Write objection-flip Reel script**

  Use your saved Week 3 Q&A responses. Pick the top theme. Example:
  ```
  "You told me your biggest struggle was getting stopped out before the move.

  Here's how the AW Indicator fixes exactly that.

  [Show the liquidity zone feature — stops outside the zone before entry]

  Sept 1 — awtrading.com/indicator"
  ```
  Film and save to `Raw Footage/W6-reel2-objection.mp4`

- [ ] **Step 5: Film Reel #1 — announcement Reel**

  30 seconds. Show the indicator on chart. Text overlay: "$39/mo — Sept 1."
  Voiceover: "AW Indicator drops September 1. Link in bio for details."
  Save to `Raw Footage/W6-reel1-announce.mp4`

- [ ] **Step 6: Edit all content**

### Monday Aug 10

- [ ] **Step 7: Post Reel #1 — announcement**

  Caption:
  ```
  AW Indicator drops September 1 🚀

  $39/mo — indicator access
  $129/mo — indicator + Live Trader mentorship

  Details → awtrading.com/indicator

  #indicator #futurestrading #ICT #daytrading
  ```

### Wednesday Aug 12

- [ ] **Step 8: Upload YouTube reveal video**

  Pin a comment with the Whop link.
  Post the reveal in Discord #sept-1-launch: "Full reveal just dropped on YouTube → [link]"

- [ ] **Step 9: Post IG Story series (3 parts)**

  Story 1: Show indicator feature — session levels auto-drawing. Text: "It does this 👇"
  Story 2: Show signal feature. Text: "And this."
  Story 3: Text only. "September 1. Join Discord for early access → link in bio"

### Friday Aug 14

- [ ] **Step 10: Post Reel #2 — objection flip**

  Caption:
  ```
  You told me your biggest struggle was [X] 👇

  Here's how the AW Indicator fixes exactly that.

  [1 sentence on the feature shown]

  Sept 1 → awtrading.com/indicator
  ```

- [ ] **Step 11: Discord #sept-1-launch engagement post**

  ```
  Who's planning to grab the indicator on Sept 1?

  Drop a 🔥 if you're in.
  ```
  Screenshot the replies — use for Week 7 social proof content.

### Sunday Aug 16 — Weekly Review

- [ ] **Step 12: Log metrics** (YouTube reveal views are your highest-intent audience — note this)

- [ ] **Step 13: Week 7 prep**

  ```
  ⬜ Book 2-hour filming session Tuesday Aug 18
  ⬜ Identify 5–7 live trade clips from this week for daily Reels
  ⬜ Confirm indicator is ready for a raw live session recording
  ```

---

## Task 7: Week 7 — Build Heat (Aug 17–23)

**Theme:** Volume over polish. One clip per day. The market open is your content.

### Tuesday Aug 19 — Batch Film Day

- [ ] **Step 1: Record raw live trading session with the indicator**

  Film a full session (or partial — 30 min minimum) with indicator on screen.
  Do not edit for performance — keep it raw and real.
  Save to `Raw Footage/W7-youtube-live-session.mp4`

- [ ] **Step 2: Film Short — "Why I built this indicator"**

  60 seconds. Personal story. Camera face (not screen).
  ```
  "I built this because I kept seeing the same problem — [your experience].
  I wanted one tool that showed me [what it shows].
  September 1 it's available to everyone. Link in bio."
  ```
  Save to `Raw Footage/W7-short-why-i-built.mp4`

- [ ] **Step 3: Prepare 5 Reel clips from week's trade footage**

  Pull 5 different signal/outcome clips. 15–30 sec each.
  Label: `W7-reel-mon.mp4`, `W7-reel-tue.mp4`, etc.
  Edit all: add captions, add countdown text overlay ("X days until launch").

### Monday Aug 17 through Friday Aug 21 — Daily Posts

- [ ] **Step 4: Post one Reel per day (Monday–Friday)**

  Day 1 caption:
  ```
  Day 1 of posting this daily until launch 🔥

  [Brief description of signal/outcome]

  Sept 1 → awtrading.com/indicator
  ```

  Days 2–5 caption formula:
  ```
  Day [N] 📈 [brief description]

  [X] days until launch → awtrading.com/indicator
  ```

### Wednesday Aug 19

- [ ] **Step 5: Upload YouTube live session + Short**

  Title: `Trading Live With the AW Indicator — Raw Session Footage`
  Pin comment: Whop link.

### Thursday Aug 20

- [ ] **Step 6: Post objection Reel — "Is $39/mo worth it?"**

  Caption:
  ```
  Is $39/mo worth it? 👇

  Here's what it did in a single session:
  [Outcome from this week's live session]

  You decide. Sept 1 → awtrading.com/indicator

  #trading #indicator #futurestrading
  ```

- [ ] **Step 7: Post Instagram countdown sticker Story**

  Add Instagram countdown sticker. Label: "AW Indicator Launch". Set to Sept 1, 2026.
  Followers can subscribe — they get a push notification at launch.
  Caption: "Launching in…"

### Friday Aug 21

- [ ] **Step 8: Discord reminder post in #sept-1-launch**

  ```
  11 days.

  The indicator goes live Sept 1.

  Grab it here: [Whop link]

  $39/mo — indicator
  $129/mo — indicator + Live Trader

  Discord members get access the moment it goes live.
  ```

- [ ] **Step 9: Populate #testimonials if not already done**

  Add 3–5 more P&L screenshots, certs, and prop passes.
  Each post: "Here's what's possible." No over-explaining.

### Sunday Aug 23 — Weekly Review + Launch Prep

- [ ] **Step 10: Log metrics** (Reel reach this week should be your highest — note it)

- [ ] **Step 11: Launch day draft content**

  Write all launch day posts now so Sept 1 morning is just copy-paste:

  IG Reel caption:
  ```
  It's live. 🚀

  AW Indicator — awtrading.com/indicator
  $39/mo indicator
  $129/mo indicator + Live Trader

  Link in bio.
  ```

  Discord #general:
  ```
  🚀 It's live.

  AW Indicator + Live Trader are now available.

  Grab it: [Whop link]
  ```

  Discord #sept-1-launch:
  ```
  IT'S LIVE. [Whop link] — go get it 🔥
  ```

  Save all of these in a notes app on your phone.

- [ ] **Step 12: Final tech checklist**

  ```
  ⬜ Whop products — publish or schedule for Sept 1 midnight
  ⬜ YouTube Live — schedule stream for Sept 1, 9:30am
  ⬜ Test Whop purchase flow from a fresh browser (incognito)
  ⬜ Confirm awtrading.com/indicator page links to the correct Whop URL
  ⬜ Make sure IG morning Reel is filmed and ready to post 8:30am
  ```

---

## Task 8: Final Push (Aug 24–31)

**Theme:** Sustain momentum. Don't go dark. One post every 1–2 days.

- [ ] **Step 1: Every-other-day Reel through Aug 31**

  Content options (pick one per post):
  - Countdown clip: "X days until launch 🚀"
  - Another indicator signal clip
  - "If you're on the fence, here's who this is for" — describe the ideal customer
  - Discord hype screenshot (blur usernames if needed)

- [ ] **Step 2: Discord check-in every 2–3 days**

  Post in #sept-1-launch to keep energy up:
  "5 days. Getting close."
  "3 days. Making sure everything is ready."
  "Tomorrow. See you at the open."

- [ ] **Step 3: Night before — Aug 31 launch prep**

  Run through the full pre-launch checklist:
  ```
  ⬜ Whop products live (or scheduled for 12:00am Sept 1)
  ⬜ Morning IG Reel ready (film if not done)
  ⬜ Discord announcements written and saved in notes
  ⬜ YouTube live stream scheduled (title: "AW Indicator is LIVE — trading the open 🚀")
  ⬜ Website working — open awtrading.com/indicator, confirm Whop link works
  ⬜ Charged laptop, stable internet confirmed
  ```

---

## Task 9: Launch Day — September 1, 2026

**Execute in this exact order.**

- [ ] **Step 1: 8:30am — Post IG Reel**

  Use the pre-written caption from Task 7 Step 11.
  Post immediately. Then post a Story: "It's live — link in bio 👆"

- [ ] **Step 2: 9:00am — Discord announcements**

  Paste pre-written posts into all three channels simultaneously:
  - `#general`
  - `#sept-1-launch`
  - Update pin in `#start-here` to include the Whop link

- [ ] **Step 3: 9:30am — Go live on YouTube**

  Title: `AW Indicator is LIVE — Trading the Open Right Now 🚀`
  Drop the Whop link in chat every 10 minutes.
  Trade live. Keep commentary going. Aim for 30–60 minutes.

- [ ] **Step 4: During the stream — Stories**

  Every 15–20 min, post a Story update: "We're live — watch on YouTube"

- [ ] **Step 5: After stream ends**

  Clip best 2-minute segment → upload as YouTube Short immediately.
  Post that clip to Instagram Reels (caption: "[X] people already in the first hour 🔥").
  Post that clip to Discord #sept-1-launch.

- [ ] **Step 6: Afternoon — Story updates**

  Post Stories every 2 hours:
  - Member count update: "X people joined today"
  - A live trade from today's session
  - Whop link reminder

- [ ] **Step 7: Reply to everything**

  Reply to every DM, every comment, every Discord message today.
  This is the highest-leverage use of your time on launch day.

---

## Task 10: Post-Launch (Sept 2+)

- [ ] **Step 1: Day-after review (Sept 2)**

  Log:
  ```
  Launch Day Metrics
  Whop sign-ups — indicator: ___
  Whop sign-ups — Live Trader: ___
  YouTube live peak viewers: ___
  IG Reel launch views: ___
  Discord member delta: ___
  Which post drove the most Whop traffic: ___
  ```

- [ ] **Step 2: Thank-you content**

  Post a Story thanking everyone who joined.
  Post in Discord: "Welcome to everyone who joined. Here's what's coming…"

- [ ] **Step 3: Keep posting**

  The launch window is 7 days, not 1.
  Post every day Sept 1–7. Content: member wins, live sessions, onboarding tips.

- [ ] **Step 4: Update website post-launch**

  The countdown bar auto-updates to "now live!" text on Sept 1.
  Update the indicator page Whop link if the URL changed.

  ```bash
  # If you need to update the Whop link:
  # Edit indicator.html — find the "Buy Now" / Whop link
  # Update the href
  git add indicator.html
  git commit -m "Update Whop link post-launch"
  git push origin master
  ```

---

## Metrics Tracker Template

Copy this into a spreadsheet. Fill in each Sunday.

| Week | YT Views | YT Subs Δ | IG Reel 1 Reach | IG Reel 2 Reach | Discord Members | Notes |
|---|---|---|---|---|---|---|
| W1 Jul 6–12 | | | | | | |
| W2 Jul 13–19 | | | | | | |
| W3 Jul 20–26 | | | | | | |
| W4 Jul 27–Aug 2 | | | | | | |
| W5 Aug 3–9 | | | | | | |
| W6 Aug 10–16 | | | | | | |
| W7 Aug 17–23 | | | | | | |
| Final Aug 24–31 | | | | | | |
| Launch Sept 1 | | | | | | |

---

## Task 11: Membership Content — Private Filming (Thursdays)

**Prerequisite for students:** Must already understand market structure, FVGs, BOS, basic ICT. This curriculum develops judgment and edge — not basics.

### Thu Jul 10 — Module 1: Why Price Does What It Does

- [ ] **Step 1: Film Module 1 (45–60 min of content, 2–3 videos)**

  Topics to cover across the videos:
  - Institutional order flow as the actual driver of price
  - Why retail setups fail — what's really happening behind them
  - How to read a move: delivery, expansion, retracement
  - The difference between reacting to price and anticipating it
  - Why context (what came before) matters more than the pattern itself

  Save to `AW Trading Content/Raw Footage/Private/M1-why-price/`

- [ ] **Step 2: Note one strong concept to tease publicly**

  Identify one idea from Module 1 that you can reference in public content (without giving the full lesson). This creates a trail from free content → paid curriculum.

### Thu Jul 17 — Module 2: Building Your Data Collection System

- [ ] **Step 1: Film Module 2 (30–45 min, 2 videos)**

  Topics:
  - What data actually matters vs. what's noise
  - How to log a trade: entry/exit/P&L + the read, context, and emotional state
  - Tracking by session, instrument, and time of day
  - The weekly review ritual — what patterns to look for
  - How to extract useful information from a losing trade

  Save to `AW Trading Content/Raw Footage/Private/M2-data-collection/`

- [ ] **Step 2: Write trade log template (PDF)**

  Fields to include:
  ```
  Date / Instrument / Session
  Pre-trade read: [What did you think was happening?]
  Entry reason: [Why here, not earlier or later?]
  Result: [P&L + did price do what you expected?]
  Deviation: [Did you follow your plan? If not, why?]
  Lesson: [One sentence]
  ```
  Save as `AW Trading Content/Assets/Playbooks/trade-log-template.pdf`

### Thu Jul 24 — Module 3: Finding Your Edge in the Data

- [ ] **Step 1: Film Module 3 (30–40 min, 2 videos)**

  Topics:
  - How to review a month of trades and find real patterns
  - Identifying your highest-probability conditions (session, setup type, time)
  - The difference between a market edge and a personal edge
  - When to stop trading a setup that your data says isn't working for you
  - How to narrow your playbook based on what your own data shows

  Save to `AW Trading Content/Raw Footage/Private/M3-finding-edge/`

- [ ] **Step 2: Write monthly data review framework (PDF)**

  Questions to include:
  ```
  1. Which session was most profitable? Least?
  2. Which setup type had the highest win rate?
  3. What time of day were your worst trades?
  4. Where did you deviate from your plan — and what triggered it?
  5. What is one setup to cut this month based on the data?
  6. What is one condition to press harder based on the data?
  ```
  Save as `AW Trading Content/Assets/Playbooks/monthly-review-framework.pdf`

### Thu Jul 31 — Module 4: Psychology — Understanding Yourself as the Variable

- [ ] **Step 1: Film Module 4 (30–40 min, 2 videos)**

  Topics:
  - Why you deviate from your plan and what that reveals about you
  - Recognizing your personal tilt triggers (loss streaks, FOMO, revenge)
  - The pre-trade mental checklist — not rules, but self-awareness
  - How to process a losing streak without destroying your edge
  - The self-honesty gap: what you think you do vs. what you actually do

  Save to `AW Trading Content/Raw Footage/Private/M4-psychology/`

- [ ] **Step 2: Write psychology self-audit (PDF)**

  Format:
  ```
  Run this monthly. Answer honestly.

  1. What was my most common reason for deviating from my plan?
  2. What emotional state preceded my worst trades?
  3. Did I revenge trade? What triggered it?
  4. Did I cut winners early? What was I afraid of?
  5. On my best trading days, what was different about my mindset?
  6. One thing I will do differently next month:
  ```
  Save as `AW Trading Content/Assets/Playbooks/psychology-self-audit.pdf`

### Thu Aug 7 — Module 5: Building Discretion

- [ ] **Step 1: Film Module 5 (30–40 min, 2 videos)**

  Topics:
  - What discretion actually means (it's not guessing — it's informed judgment)
  - Reading confluence without running through a checklist
  - When the setup is technically valid but the read says don't take it
  - How to develop conviction — knowing when you actually have edge
  - The role of patience: not every session needs a trade

  Deliver primarily through chart walkthroughs and real examples. Minimize definitions.
  Save to `AW Trading Content/Raw Footage/Private/M5-discretion/`

- [ ] **Step 2: Write risk and sizing guide (PDF)**

  ```
  Sizing by conviction — not a fixed rule:

  High conviction (A+ setup, context confirms, clean structure):
  → Full size
  High conviction but one condition missing:
  → 75% size
  Moderate conviction (setup valid, context unclear):
  → 50% size or skip
  Low conviction / forcing it:
  → Do not trade

  When to scale up: 3+ consecutive weeks of positive data
  When to scale down: 2+ consecutive losing days, or any emotional deviation
  Max daily loss: [set your own number — stop trading when hit, no exceptions]
  ```
  Save as `AW Trading Content/Assets/Playbooks/risk-sizing-guide.pdf`

### Thu Aug 14 — Module 6: Advanced Concepts — What I've Actually Picked Up

- [ ] **Step 1: Plan your advanced concepts before filming**

  Write out 4–6 observations you've made beyond standard ICT. These should be:
  - Things you figured out through your own trading, not things you learned from someone else
  - Specific enough to be actionable, not vague principles
  - Things that would surprise even an experienced ICT trader

  These are the most valuable thing in your curriculum. Don't rush this step.

- [ ] **Step 2: Film Module 6 (45–60 min, 3–4 videos)**

  Structure:
  - Video 1: Your advanced observations (2–3 concepts)
  - Video 2: What you've learned specifically from your losing trades
  - Video 3: How you read sessions differently now vs. when you started
  - Video 4: How to keep evolving after the mentorship — your learning process

  Save to `AW Trading Content/Raw Footage/Private/M6-advanced/`

- [ ] **Step 3: Write pre-session framework (PDF)**

  ```
  Before every session — not a checklist, a thinking process:

  1. What is the higher timeframe narrative? (Who has control — buyers or sellers?)
  2. Where is the liquidity resting above and below price?
  3. What would price need to do to confirm the narrative?
  4. What session am I trading and what does that session typically deliver?
  5. What is my read? (Write it down before the open.)
  6. Am I in a state to trade today? (Check psychology self-audit triggers.)

  After the session:
  - Did price confirm your narrative?
  - If not, where was the read wrong?
  - Log the trade.
  ```
  Save as `AW Trading Content/Assets/Playbooks/pre-session-framework.pdf`

### Sat Aug 22 — Edit All Modules + Upload to Whop

- [ ] **Step 1: Edit all 6 modules**

  Priority order: M1 → M6 (edit them in sequence).
  Each video: trim dead air, add chapter titles as text overlays. No heavy production needed — clean audio and clear screen is enough.
  Export all at 1080p. Save to `AW Trading Content/Edited/Private/`

- [ ] **Step 2: Upload to Whop**

  In Whop dashboard: create the Live Trader product course section.
  Upload modules in order. Set access to $129/mo tier only.
  Upload all 5 PDFs to a resources section.

- [ ] **Step 3: Create members-only Discord channels**

  Create all 6 channels in Discord:
  - `#live-trader-lounge` — set role access to $129/mo members only
  - `#trade-alerts` — same role restriction
  - `#trade-journal` — same role restriction
  - `#resources` — pin all 5 PDF playbooks here immediately
  - `#weekly-live` — for session replay links post-launch
  - `#indicator-users` — set role access to $39/mo+ members

### Week 8 (Aug 24–31) — QA and Final Prep

- [ ] **Step 1: Watch every module from start to finish**

  Watch as a student would. Note anything confusing or missing.
  Fix any issues before Sept 1.

- [ ] **Step 2: Test Whop member access**

  Create a test account or use a second device.
  Purchase the $39 tier and verify indicator access + #indicator-users channel.
  Purchase the $129 tier and verify curriculum access + all members channels + PDFs.

- [ ] **Step 3: Write the welcome message**

  Draft what $129/mo members see immediately after purchase:
  ```
  Welcome to Live Trader.

  Here's where to start:
  1. Introduce yourself in #live-trader-lounge
  2. Download your resources in #resources — start with the trade log template
  3. Begin Module 1 in the course section
  4. Our first live session is [date] at [time]

  This curriculum assumes you know the basics. If you're starting from zero,
  the $39 indicator tier + the free Discord is the right place to begin.
  ```

- [ ] **Step 4: Schedule first post-launch live session**

  Pick a date in the first week of September for the first live session.
  Add it to Google Calendar. Post in #weekly-live on Sept 1 with the date.
