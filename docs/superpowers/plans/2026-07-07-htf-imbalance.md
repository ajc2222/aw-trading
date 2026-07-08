# HTF Imbalance Indicator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a standalone Pine Script v6 indicator that detects the highest-timeframe FVG price is currently mitigating and draws it as a single live-updating rectangle.

**Architecture:** A reusable `f_scan()` function runs inside five `request.security()` calls (one per TF: D, 4H, 1H, 15m, 5m). Each call returns the 3 most recent non-inverted FVGs for that TF. The chart-level resolution loop walks TFs top-down and finds the first zone that contains the current price. One `var box` is maintained — created when a zone activates, extended each bar, deleted when price exits.

**Tech Stack:** Pine Script v6, TradingView

---

## Task 1: File Skeleton, Settings, and Helpers

**Files:**
- Create: `src/indicator/aw-htf-imbalance.pine`

- [ ] **Step 1: Create the file with indicator declaration and settings**

```pine
//@version=6
indicator("AW HTF Imbalance", overlay=true, max_bars_back=500)

// ═══════════════════════════════════════════════════════════════════
// SETTINGS
// ═══════════════════════════════════════════════════════════════════
g = "HTF Imbalance"
zone_col   = input.color(color.new(#888888, 70), "Zone Color",   group=g)
show_label = input.bool(true, "Show Label",                       group=g)
label_col  = input.color(color.white, "Label Color",             group=g)
label_size = input.string("small", "Label Size",
              options=["tiny","small","normal","large"],           group=g)
lookback   = input.int(100, "Lookback (HTF bars)",
              minval=10, maxval=500,                               group=g)

// ═══════════════════════════════════════════════════════════════════
// HELPERS
// ═══════════════════════════════════════════════════════════════════
f_size(string s) =>
    switch s
        "tiny"   => size.tiny
        "small"  => size.small
        "normal" => size.normal
        "large"  => size.large
        => size.small
```

- [ ] **Step 2: Paste into TradingView Pine Script editor and confirm it compiles with no errors**

Expected: green "No errors" message. Settings panel shows "HTF Imbalance" group with 5 inputs.

- [ ] **Step 3: Commit**

```bash
git add src/indicator/aw-htf-imbalance.pine
git commit -m "Add HTF Imbalance indicator skeleton and settings"
```

---

## Task 2: FVG Scan Function

**Files:**
- Modify: `src/indicator/aw-htf-imbalance.pine`

This function runs inside `request.security()` so all series references (`high`, `low`, `close`, `time`) refer to the HTF timeframe. Dynamic indexing (`high[i]` where `i` is a runtime variable) is valid here because `max_bars_back=500` is set on the indicator.

- [ ] **Step 1: Add `f_scan()` after the helpers section**

```pine
// ═══════════════════════════════════════════════════════════════════
// FVG SCAN — runs in HTF context via request.security()
// Returns 3 most recent non-inverted FVGs as flat tuple:
//   [top1, bot1, time1, top2, bot2, time2, top3, bot3, time3]
// Values are `na` if fewer than 3 zones found.
// ═══════════════════════════════════════════════════════════════════
f_scan(int lb) =>
    float t1  = na
    float b1  = na
    int   tm1 = na
    float t2  = na
    float b2  = na
    int   tm2 = na
    float t3  = na
    float b3  = na
    int   tm3 = na
    int   found = 0

    for i = 0 to lb
        if found >= 3
            break
        if na(high[i + 2])
            break

        // ── Bullish FVG: bar[i] low > bar[i+2] high ──────────────
        if low[i] > high[i + 2]
            float bot = high[i + 2]
            float top = low[i]
            bool  inv = false
            if i > 0
                for j = 0 to i - 1
                    if close[j] < bot
                        inv := true
                        break
            if not inv
                if found == 0
                    t1  := top
                    b1  := bot
                    tm1 := time[i]
                else if found == 1
                    t2  := top
                    b2  := bot
                    tm2 := time[i]
                else
                    t3  := top
                    b3  := bot
                    tm3 := time[i]
                found += 1

        // ── Bearish FVG: bar[i] high < bar[i+2] low ──────────────
        if found < 3 and high[i] < low[i + 2]
            float top = low[i + 2]
            float bot = high[i]
            bool  inv = false
            if i > 0
                for j = 0 to i - 1
                    if close[j] > top
                        inv := true
                        break
            if not inv
                if found == 0
                    t1  := top
                    b1  := bot
                    tm1 := time[i]
                else if found == 1
                    t2  := top
                    b2  := bot
                    tm2 := time[i]
                else
                    t3  := top
                    b3  := bot
                    tm3 := time[i]
                found += 1

    [t1, b1, tm1, t2, b2, tm2, t3, b3, tm3]
```

- [ ] **Step 2: Verify compilation in TradingView**

Paste updated file. Expected: no errors. (No visible output yet — security calls come in Task 3.)

- [ ] **Step 3: Commit**

```bash
git add src/indicator/aw-htf-imbalance.pine
git commit -m "Add HTF FVG scan function"
```

---

## Task 3: Security Calls and Top-Down Resolution

**Files:**
- Modify: `src/indicator/aw-htf-imbalance.pine`

All `request.security()` calls must be at the top level (not inside conditionals or functions).

- [ ] **Step 1: Add the five security calls after `f_scan()`**

```pine
// ═══════════════════════════════════════════════════════════════════
// HTF DATA — top level, no lookahead
// ═══════════════════════════════════════════════════════════════════
[t1_d,  b1_d,  tm1_d,  t2_d,  b2_d,  tm2_d,  t3_d,  b3_d,  tm3_d]  = request.security(syminfo.tickerid, "D",   f_scan(lookback), lookahead=barmerge.lookahead_off)
[t1_4h, b1_4h, tm1_4h, t2_4h, b2_4h, tm2_4h, t3_4h, b3_4h, tm3_4h] = request.security(syminfo.tickerid, "240", f_scan(lookback), lookahead=barmerge.lookahead_off)
[t1_1h, b1_1h, tm1_1h, t2_1h, b2_1h, tm2_1h, t3_1h, b3_1h, tm3_1h] = request.security(syminfo.tickerid, "60",  f_scan(lookback), lookahead=barmerge.lookahead_off)
[t1_15, b1_15, tm1_15, t2_15, b2_15, tm2_15, t3_15, b3_15, tm3_15] = request.security(syminfo.tickerid, "15",  f_scan(lookback), lookahead=barmerge.lookahead_off)
[t1_5,  b1_5,  tm1_5,  t2_5,  b2_5,  tm2_5,  t3_5,  b3_5,  tm3_5]  = request.security(syminfo.tickerid, "5",   f_scan(lookback), lookahead=barmerge.lookahead_off)
```

- [ ] **Step 2: Add the top-down resolution logic**

```pine
// ═══════════════════════════════════════════════════════════════════
// TOP-DOWN RESOLUTION
// Walk D → 4H → 1H → 15 → 5, return highest TF zone price is inside
// ═══════════════════════════════════════════════════════════════════
f_in(float t, float b) => not na(t) and close >= b and close <= t

// Return first zone (most recent) that contains current close
f_resolve(float t1, float b1, int tm1,
          float t2, float b2, int tm2,
          float t3, float b3, int tm3) =>
    float zt  = na
    float zb  = na
    int   ztm = na
    if f_in(t1, b1)
        zt  := t1
        zb  := b1
        ztm := tm1
    else if f_in(t2, b2)
        zt  := t2
        zb  := b2
        ztm := tm2
    else if f_in(t3, b3)
        zt  := t3
        zb  := b3
        ztm := tm3
    [zt, zb, ztm]

// Check each TF in priority order
float  act_top = na
float  act_bot = na
int    act_tm  = na
string act_lbl = na

[rd_t,  rd_b,  rd_tm]  = f_resolve(t1_d,  b1_d,  tm1_d,  t2_d,  b2_d,  tm2_d,  t3_d,  b3_d,  tm3_d)
[r4_t,  r4_b,  r4_tm]  = f_resolve(t1_4h, b1_4h, tm1_4h, t2_4h, b2_4h, tm2_4h, t3_4h, b3_4h, tm3_4h)
[r1_t,  r1_b,  r1_tm]  = f_resolve(t1_1h, b1_1h, tm1_1h, t2_1h, b2_1h, tm2_1h, t3_1h, b3_1h, tm3_1h)
[r15_t, r15_b, r15_tm] = f_resolve(t1_15, b1_15, tm1_15, t2_15, b2_15, tm2_15, t3_15, b3_15, tm3_15)
[r5_t,  r5_b,  r5_tm]  = f_resolve(t1_5,  b1_5,  tm1_5,  t2_5,  b2_5,  tm2_5,  t3_5,  b3_5,  tm3_5)

if not na(rd_t)
    act_top := rd_t
    act_bot := rd_b
    act_tm  := rd_tm
    act_lbl := "1D"
else if not na(r4_t)
    act_top := r4_t
    act_bot := r4_b
    act_tm  := r4_tm
    act_lbl := "4H"
else if not na(r1_t)
    act_top := r1_t
    act_bot := r1_b
    act_tm  := r1_tm
    act_lbl := "1H"
else if not na(r15_t)
    act_top := r15_t
    act_bot := r15_b
    act_tm  := r15_tm
    act_lbl := "15"
else if not na(r5_t)
    act_top := r5_t
    act_bot := r5_b
    act_tm  := r5_tm
    act_lbl := "5"
```

- [ ] **Step 3: Verify compilation in TradingView**

Paste updated file. Expected: no errors. Still no visible output until Task 4.

- [ ] **Step 4: Commit**

```bash
git add src/indicator/aw-htf-imbalance.pine
git commit -m "Add security calls and top-down TF resolution"
```

---

## Task 4: Box Display — Live Updating

**Files:**
- Modify: `src/indicator/aw-htf-imbalance.pine`

The box uses `xloc.bar_time` so its left edge is anchored to the timestamp of the HTF bar where the FVG formed. The right edge is extended to `timenow` + a buffer on every bar for live updates. The box is recreated only when the active zone changes — otherwise just `box.set_right()` is called.

- [ ] **Step 1: Add the box display logic at the end of the file**

```pine
// ═══════════════════════════════════════════════════════════════════
// DISPLAY — single box, live-updating
// ═══════════════════════════════════════════════════════════════════
var box   active_box = na
var float prev_top   = na
var float prev_bot   = na

// Right edge: current time + 50 chart bars worth of ms
right_ms = timenow + timeframe.in_seconds() * 1000 * 50

zone_changed = act_top != prev_top or act_bot != prev_bot
zone_active  = not na(act_top)

if zone_active
    if na(active_box) or zone_changed
        if not na(active_box)
            box.delete(active_box)
        active_box := box.new(
             left         = act_tm,
             top          = act_top,
             right        = right_ms,
             bottom       = act_bot,
             xloc         = xloc.bar_time,
             bgcolor      = zone_col,
             border_color = color.new(color.white, 100),
             border_width = 0,
             text         = show_label ? act_lbl : "",
             text_color   = label_col,
             text_size    = f_size(label_size),
             text_halign  = text.align_right,
             text_valign  = text.align_center)
        prev_top := act_top
        prev_bot := act_bot
    else
        box.set_right(active_box, right_ms)
else
    if not na(active_box)
        box.delete(active_box)
        active_box := na
    prev_top := na
    prev_bot := na
```

- [ ] **Step 2: Full test in TradingView — Zone appears**

On a 1m or 5m chart of NQ or ES:
- Navigate to a period where price was inside a higher-TF FVG
- Verify a grey rectangle appears covering the FVG zone
- Verify the label shows the correct TF (`1D`, `4H`, `1H`, `15`, or `5`)
- Verify only one rectangle is visible at a time

- [ ] **Step 3: Test — Zone disappears when price exits**

Scroll to a candle that moved out of a known FVG zone (without inverting it). Verify the rectangle is not drawn there (it should only appear while price was inside).

- [ ] **Step 4: Test — Higher TF wins when nested**

Find a spot where price was inside both a 1H and a 4H FVG simultaneously. Verify the rectangle shows `4H`, not `1H`.

- [ ] **Step 5: Test — Settings work**

Change zone color, toggle label off, change label size. Verify each setting applies correctly.

- [ ] **Step 6: Commit**

```bash
git add src/indicator/aw-htf-imbalance.pine
git commit -m "Add live-updating box display for HTF Imbalance indicator"
```

---

## Task 5: Edge Case Verification and Final Commit

**Files:**
- Modify: `src/indicator/aw-htf-imbalance.pine` (if any fixes needed)

- [ ] **Step 1: Test — Inverted FVG is excluded**

Find a zone that was inverted (a subsequent HTF candle closed through the full zone). Verify the indicator does NOT display that zone even if price re-enters that price range later.

- [ ] **Step 2: Test — Lookback setting**

Set lookback to 10 and verify fewer historical FVGs are found. Set to 200 and verify deeper history is scanned. No compile errors at either value.

- [ ] **Step 3: Test — Live bar updates**

On a live chart, move to the current bar and verify the rectangle appears immediately when price enters a zone (without waiting for the candle to close).

- [ ] **Step 4: Final commit**

```bash
git add src/indicator/aw-htf-imbalance.pine
git commit -m "AW HTF Imbalance indicator complete — top-down scan, live updates, inverted FVG exclusion"
```
