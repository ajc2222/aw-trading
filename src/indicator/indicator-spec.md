# AW Indicator — Full Feature Spec

**Platform:** TradingView (Pine Script v6)  
**File:** `src/indicator/aw-indicator.pine`  
**Launch deadline:** August 3, 2026 (must be tease-ready on camera)  
**Fully polished by:** August 10, 2026 (reveal video)

---

## Product Decision: One Indicator

All ICT and QT features ship in a single indicator with clearly separated settings groups. QT features are toggled independently. If QT logic exceeds 150 lines, evaluate splitting into a companion script — but default is one product.

---

## Features

### 1. CISD — Change in State of Delivery ✅ DONE
Detects when price has shifted from delivery to retracement (or vice versa).
Draws a horizontal line at the open of the leg that triggered the shift.
Settings group: "CISD Settings"

### 2. IFVG — Inverse Fair Value Gap ✅ DONE
Detects fair value gaps within the leg identified by CISD.
Draws filled rectangles for IFVGs, filtered to the relevant leg only.
Settings group: "IFVG Settings"

### 3. Session Liquidity 🔄 IN PROGRESS
**What it does:**
- Mark session highs and lows for Asia, London, and New York sessions
- Draw horizontal lines at each session's high and low
- When price sweeps (closes beyond) a session high or low, mark the sweep visually (change line style, add label)
- Option to show/hide each session independently

**Settings group:** "Session Liquidity"
**Inputs:**
- Show Asia liquidity (bool, default true)
- Show London liquidity (bool, default true)
- Show NY liquidity (bool, default true)
- Buy-side color (default green)
- Sell-side color (default red)
- Show sweep labels (bool, default true)

**Session times (UTC):**
- Asia: 00:00–08:00
- London: 07:00–12:00
- New York: 12:00–17:00

---

### 4. HTF Imbalance Levels
**What it does:**
Fetches fair value gaps (imbalances) from a higher timeframe and draws them on the current chart. Unlike the IFVG feature (which is leg-filtered on the current TF), these are raw HTF FVGs — they represent unfilled imbalances on a larger context chart.

**Key behavior:** The level only becomes visible (or changes color/style) when current price is actively entering/mitigating the zone. Levels that have already been fully mitigated are either hidden or marked as closed.

**Logic:**
- Fetch OHLC from a user-selected HTF using `request.security()`
- Detect bullish FVG on HTF: `htf_low > htf_high[2]` (gap between bar[0] low and bar[2] high)
- Detect bearish FVG on HTF: `htf_high < htf_low[2]`
- Draw the zone as a box on the current TF chart
- Zone is "inactive" (muted/hidden) until current price enters it
- When price enters the zone → activate it (highlight, change opacity/border)
- When price closes beyond the midpoint of the zone → mark as mitigated (dashed outline or remove)

**Inputs:**
- HTF source (default: "60" = 1H; options: 15, 30, 60, 240, D)
- Show bullish HTF imbalances (bool)
- Show bearish HTF imbalances (bool)
- Inactive zone color (muted, low opacity — visible but not distracting)
- Active/mitigating zone color (highlighted)
- Mitigated zone: hide or show dashed (dropdown)
- Max zones to display (int, default 5)

**Settings group:** "HTF Imbalance"

**Note:** Use `request.security()` with `lookahead=barmerge.lookahead_off` to avoid repainting. Box drawing must use confirmed HTF bar data only.

---

### 5. PSP — Precision Swing Point
**What it does:**
On any given bar, if one correlated asset closes bullish (close > open) and another correlated asset closes bearish (close > open) — that bar is a PSP. It is a 1-bar SMT divergence, not a swing-based one.

**Logic:**
- Compare close vs open for two user-selected symbols on each confirmed bar
- If Symbol A is bullish AND Symbol B is bearish → Bearish PSP (selling pressure divergence)
- If Symbol A is bearish AND Symbol B is bullish → Bullish PSP (buying pressure divergence)
- Mark the bar on the chart with a label or shape

**Inputs:**
- Symbol A (default: "CME_MINI:ES1!") 
- Symbol B (default: "CME_MINI:NQ1!")
- Show bullish PSP (bool, default true)
- Show bearish PSP (bool, default true)
- Label size / color

**Settings group:** "PSP Settings"

**Note:** Use `request.security()` for Symbol B data. Only fire on `barstate.isconfirmed`.

---

### 6. SMT — Smart Money Tool (Real-Time)
**What it does:**
Detects divergence at swing highs and lows between two correlated assets.

- **Bearish SMT:** Asset A makes a higher swing high, Asset B makes a lower swing high → divergence = institutional sell signal
- **Bullish SMT:** Asset A makes a lower swing low, Asset B makes a higher swing low → divergence = institutional buy signal

**Logic:**
- Use a configurable swing lookback (default: 5 bars)
- Compare swing highs/lows between primary (chart symbol) and user-defined second symbol
- Draw a label/shape at the point of divergence

**Inputs:**
- SMT Symbol (default: "CME_MINI:NQ1!")
- Swing lookback (int, default 5, min 2, max 20)
- Show bullish SMT (bool)
- Show bearish SMT (bool)
- Label color

**Settings group:** "SMT Settings"

---

### 7. Multi-Pair SMT (ES / YM / NQ)
**Extends feature 5.**
Allow the user to monitor SMT across all three indices simultaneously:
- ES vs NQ
- ES vs YM  
- NQ vs YM

Each pair is independently toggleable. When SMT fires on multiple pairs at the same bar, that is a confluence signal — optionally display a distinct "confluence SMT" label.

**Additional inputs (in SMT Settings group):**
- Enable ES/YM pair (bool)
- Enable ES/NQ pair (bool, default on)
- Enable NQ/YM pair (bool)
- YM Symbol (default: "CBOT_MINI:YM1!")
- Show confluence label when 2+ pairs fire (bool)

---

### 8. SSMT — Sequential SMT
**Extends feature 6.**
Detects when SMT divergences occur in sequence (same direction, within a defined window).

**Logic:**
- Track the last N SMT signals (configurable window, default 10 bars)
- If 2+ consecutive SMT signals are in the same direction → SSMT confirmed
- Draw a distinct SSMT label/marker at the confirmation bar
- Optionally draw a line connecting the sequential SMT points

**Inputs:**
- SSMT window (int, default 10, min 3, max 30)
- Minimum sequential signals to confirm (int, default 2)
- Show SSMT label (bool)
- SSMT line color

**Settings group:** "SSMT Settings" (sub-section under SMT)

---

### 9. QT — Quarterly Theory
**Concept (Daye's Quarterly Theory):**
The trading day/week is divided into four equal quarterly segments. Price action within each quarter follows predictable delivery patterns. SMT divergences occurring at quarterly boundaries carry higher significance.

**Implementation scope for v1:**
- Divide the session (or day) into 4 equal quarters visually
- Detect when SMT (from feature 5/6) fires at or near a quarterly boundary (within configurable tolerance)
- Flag that SMT signal as a "QT SMT" — higher conviction
- Draw subtle vertical lines or background shading to mark quarter boundaries

**Inputs:**
- Enable QT overlay (bool, default false — off by default, user opts in)
- Session for QT division: NY session only, full day, or custom hours
- Quarter boundary tolerance (bars, default 3)
- QT line color / style
- Show QT SMT labels (bool)

**Settings group:** "QT Settings"

**Note:** QT is a distinct conceptual layer. Keep it toggled off by default so it doesn't clutter the chart for users who don't use it.

---

## Technical Constraints

- `max_bars_back=1000` (already set)
- `max_boxes_count=500` (already set)
- All `request.security()` calls for external symbols must be at the top level (not inside if-blocks)
- Only fire drawing logic on `barstate.isconfirmed` to prevent repainting
- TF gate already implemented: only runs on 1–5 minute charts. Review whether SMT and QT should run on higher TFs — likely yes. Make the TF gate configurable per feature group.
- Settings groups must be clearly named and logically ordered in the UI

---

### 10. Trailing Stop Loss / Protected High-Low Formation
**File:** `src/indicator/aw-trailing-stop.pine`

**What it does:**
Trails a stop level to the swing low/high of each new CISD formation. Both the protected low (long stop) and protected high (short stop) are always visible — the active one is highlighted, the inactive one is dimmed. When a protected level is mitigated (price closes through it), that segment turns red and terminates at the mitigation candle.

**Stepping logic:**
- Trail steps are triggered by **CISD formations**, not just any swing
- **Bullish CISD fires** → trail steps to the pivot low of that CISD leg (new protected low)
- **Bearish CISD fires** → trail steps to the pivot high of that CISD leg (new protected high)
- CISD direction also determines which trail is "active" (highlighted)
- Only fires on `barstate.isconfirmed` — no repainting

**CISD detection (standalone):**
- Bullish CISD: confirmed close crosses above most recent `ta.pivothigh`
- Bearish CISD: confirmed close crosses below most recent `ta.pivotlow`
- Lookback configurable (default 5 bars each side)

**Visual behavior:**
- Both trails always draw simultaneously
- **Active trail** (matching CISD direction): solid line, full color opacity
- **Inactive trail**: dimmed to configurable opacity, or fully hidden
- Each new CISD terminates the previous segment at the current bar and starts a new one → natural staircase pattern
- **Mitigation**: when price closes beyond the protected level → that segment turns red (`color_hit`), line stops exactly at the mitigation candle, "Mitigated" label placed at that bar
- Prior staircase segments keep their original color — only the mitigated segment turns red
- After mitigation, trail resets and waits for the next CISD

**Inputs:**

*Trailing Stop group:*
- Enable (bool, default true)
- Show Inactive Trail (bool, default true)
- Line Width (1–4, default 2)
- Protected Low Color (default #26a69a)
- Protected High Color (default #ef5350)
- Mitigated Color (default #ef5350)
- Inactive Opacity % (10–90, default 60)
- Max Visible Segments (2–20, default 10)

*Labels group:*
- Show Level Labels (bool, default true) — "Protected Low" / "Protected High" on each new segment
- Show Mitigated Label (bool, default true) — "Mitigated" at the breach candle
- Label Size (Tiny / Small / Normal / Large, default Small)

*CISD / Swing Detection group:*
- Swing Lookback (2–20, default 5)

**Note:** Shipped as a standalone Pine file. When integrating into the main AW Indicator, reuse the CISD signal from Feature 1 rather than re-detecting it.

---

---

### Suggested Future Features (evaluate after v1 is complete)

These are worth considering once features 1–9 are stable:

**A. Kill Zone Shading**
Shade the chart background during high-probability ICT kill zones (London Open 7–9am UTC, NY Open 12–2pm UTC, NY PM 15–16pm UTC). Simple but high-value visual context for any user. Very low complexity to implement.

**B. HTF Bias Label**
A corner label (top-right) showing current HTF trend bias: "Bullish above [price]" or "Bearish below [price]" based on the most recent HTF CISD. Gives the user instant context without scrolling to a higher TF.

**C. Equal Highs / Equal Lows (EQH/EQL) Detection**
Detect when price forms two highs or lows within a small tolerance range. These are liquidity magnets. Draw a dashed line with a label. Simple to implement, highly visible on content.

**D. Displacement Detection**
Flag when a candle (or series of candles) moves aggressively in one direction — a "displacement" away from a range. Often precedes an IFVG or OB test. Medium complexity.

**E. Market Structure Shift (MSS) + Break of Structure (BOS)**
Detect when price takes out a prior swing high/low with a close (MSS) vs. a wick (BOS). These are already in ICT vocabulary and complement CISD well. Many users will expect this.

---

## Settings Panel Order (UI)

1. CISD Settings
2. IFVG Settings
3. HTF Imbalance
4. Session Liquidity
5. PSP Settings
6. SMT Settings (includes multi-pair + SSMT subsection)
7. QT Settings

---

## Delegation Instructions

When handing this to a Pine Script agent, provide:
1. This spec file
2. The current indicator code: `src/indicator/aw-indicator.pine`
3. Tell the agent which feature to implement next (follow the numbered order above)
4. After each feature: test on a 1m or 5m ES chart with NQ pulled in for SMT features
5. Commit after each feature is working

**Agent prompt template:**
> "I'm building the AW Indicator in Pine Script v6. The current code is in `src/indicator/aw-indicator.pine`. The full feature spec is in `src/indicator/indicator-spec.md`. Please implement Feature [N]: [name]. Follow the spec exactly. Do not modify existing features. Commit when done."
