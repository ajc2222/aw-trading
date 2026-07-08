# HTF Imbalance Indicator — Design Spec

**Date:** 2026-07-07
**File:** `src/indicator/aw-htf-imbalance.pine`
**Platform:** TradingView (Pine Script v6)

---

## Purpose

Show the highest timeframe FVG that price is currently mitigating (actively inside). Only valid, non-inverted FVGs are eligible. One zone shown at a time — highest timeframe wins.

---

## Terminology

- **FVG (Fair Value Gap):** A 3-bar imbalance pattern on an HTF chart.
- **Mitigating:** Price is actively within the FVG zone (live price, not just closes). This is when the zone is shown.
- **Inverted:** A subsequent HTF candle on that same TF closes through the entire zone — bottom for bullish, top for bearish. Once inverted, the FVG is permanently invalid and never shown.

---

## Timeframe Scan Order

Top-down priority:

1. Daily (1D)
2. 4H
3. 1H
4. 15m
5. 5m

The highest TF with an active (non-inverted) FVG that price is currently inside wins. All lower TFs are ignored for that bar.

---

## FVG Detection

All detection runs on confirmed HTF bar data only (`lookahead=barmerge.lookahead_off`) to prevent repainting.

**Bullish FVG** (gap up — price left a gap on the way up):
- Condition: `htf_low[0] > htf_high[2]`
- Zone: bottom = `htf_high[2]`, top = `htf_low[0]`

**Bearish FVG** (gap down — price left a gap on the way down):
- Condition: `htf_high[0] < htf_low[2]`
- Zone: top = `htf_low[2]`, bottom = `htf_high[0]`

---

## Inversion Check

For each FVG found, scan all subsequent HTF bars forward from its formation bar:

- **Bullish FVG inverted if:** any subsequent HTF close < zone bottom
- **Bearish FVG inverted if:** any subsequent HTF close > zone top

If inverted at any point, the FVG is discarded permanently. It will never display.

---

## Scan Depth

Each TF is scanned back a configurable number of HTF bars (default: 100). This controls how far into history the script looks for valid FVGs. A daily FVG from 3 months ago can still be found and shown if it has never been inverted and price is currently inside it.

---

## Display Logic

- **Show zone:** when live price (updates tick by tick on the current bar) is inside the zone — `price >= zone.bottom and price <= zone.top`
- **Hide zone:** when price exits the zone without the FVG being inverted — zone disappears until price re-enters
- **Remove permanently:** when FVG is inverted (subsequent HTF close through entire zone)

Display runs on every bar, including the live forming bar, for real-time updates.

---

## Visual

- **Shape:** Filled rectangle, no border, no middle line
- **Left edge:** Bar index where the FVG was formed on the HTF
- **Right edge:** Current bar + 20 bar buffer (updated each bar)
- **Default color:** Grey `#888888` at 70% transparency (30% opacity)
- **Label:** TF name displayed middle-right inside the rectangle (`1D`, `4H`, `1H`, `15`, `5`)

---

## Settings

Single group: `"HTF Imbalance"`

| Input | Type | Default |
|-------|------|---------|
| Zone color | color | `#888888` at 70% transparency |
| Show label | bool | true |
| Label color | color | white |
| Label size | string (tiny/small/normal/large) | small |
| Lookback (HTF bars) | int (1–500) | 100 |

---

## Technical Notes

- Five `request.security()` calls — one per TF — all at top level (not inside conditionals)
- Scan logic runs via indexed lookback into the returned series
- Only one `box` object exists at a time; it is deleted and recreated when the active zone changes
- No `max_boxes_count` concern since at most one box is live at any time
