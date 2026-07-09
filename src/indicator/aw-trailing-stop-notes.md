# AW Trailing Stop — Logic Notes

## CISD (Change in State of Delivery)

### Bullish CISD Setup
1. A bearish leg forms (consecutive bearish candles)
2. `highest_open` = the highest open of that bearish leg — this is the CISD trigger price
3. `is_lower_low` fires: current bar's low breaks below recent structure
4. Pending state is armed: store `pend_bull_cisd_src` = bar index of the `highest_open` candle (left border)
5. Within `cisd_window` bars: if a bar closes ABOVE `highest_open` → CISD confirmed

### Bearish CISD Setup (mirror)
1. A bullish leg forms (consecutive bullish candles)
2. `lowest_open` = the lowest open of that bullish leg — CISD trigger price
3. `is_higher_high` fires
4. Pending state armed: `pend_bear_cisd_src` = bar index of the `lowest_open` candle
5. Within `cisd_window` bars: close BELOW `lowest_open` → confirmed

---

## Protected Level Placement

### Left Border
The specific candle whose open = `highest_open` (bull) or `lowest_open` (bear).
This is the CISD trigger candle — the body that price needs to close over/under.

### Right Border
The CISD confirmation candle — the bar that closes beyond the trigger.

### Manipulation Leg
- **Bull**: from the left border to the absolute lowest wick in the scan range — this is the sweep/manipulation down before the CISD confirmation.
- **Bear**: from the left border to the absolute highest wick in the scan range — the sweep up before confirmation.

### Protected Low (bull)
The absolute lowest wick across ALL bars between left border and right border (inclusive).
Candle type does not matter — wicks and bodies both count.
Line drawn from that bar's bar_index to the confirmation bar.

### Protected High (bear, mirror)
The absolute highest wick between left and right borders.

---

## Swing Divergence — `aw-swing-divergence.pine`

### What it detects
On each bar, compares ES / NQ / YM lows (bullish) or highs (bearish). If at least one index breaks below its prior low while at least one doesn't — that's a bullish swing divergence, and vice versa for bearish. All six combinations of 1-of-3 and 2-of-3 divergence are covered.

### Failure invalidation
Every drawn divergence line is stored in an array alongside its failure level:
- **Bull**: `math.min(low[1], low)` at draw time — line deleted when `low` crosses below it.
- **Bear**: `math.max(high[1], high)` at draw time — line deleted when `high` crosses above it.

### CISD Filter toggle ("Divergence Filter" settings group)
When ON, divergences only draw during an active CISD window:
- Bullish divergence → only fires while a **bullish** CISD is pending (bearish leg detected, waiting for close above trigger)
- Bearish divergence → only fires while a **bearish** CISD is pending

CISD detection is duplicated from `aw-indicator.pine` (no cross-script state sharing in Pine Script).

### Inclusive border logic
`pend_bull` is captured into `cisd_bull_prev` **before** the `barstate.isconfirmed` block runs.
The gate is `cisd_bull_prev or pend_bull` — this makes both borders inclusive:
- **Right border (confirmation bar):** `cisd_bull_prev = true`, `pend_bull = false` (just confirmed) → still allowed
- **Left border (lower-low bar):** `cisd_bull_prev = false`, `pend_bull = true` (just armed) → still allowed
- **After window:** both false → blocked

### CISD settings to match `aw-indicator.pine`
`Trigger Window` and `Max Leg Length` in the divergence script must be kept in sync with the same settings in the main indicator so both scripts agree on when a CISD is pending.

---

## FVG Partial Mitigation

### Bullish FVG (bot → top)
- Formed when: `low[i] > high[i+2]` (gap between bar[i+2] high and bar[i] low)
- Tracks `vtop` (remaining unmitigated top), starts equal to `top`
- Each bar: if `low <= vtop` → `vtop = min(vtop, low)` (wick/body entering zone shrinks it from top)
- If `vtop <= bot` → fully mitigated, remove
- If `close < bot` → inverted, remove
- If bar age > `fvg_lookback` → expired, remove
- Valid zone at any point: `bot` → `vtop`

### Bearish FVG (bot → top, price approaches from below)
- Formed when: `high[i] < low[i+2]`
- Tracks `vbot` (remaining unmitigated bottom), starts equal to `bot`
- Each bar: if `high >= vbot` → `vbot = max(vbot, high)` (shrinks zone from bottom up)
- If `vbot >= top` → fully mitigated, remove
- If `close > top` → inverted, remove
- Valid zone at any point: `vbot` → `top`

---

## FVG Tap Condition (when Require FVG Tap is ON)

At CISD confirmation time, scan every bar from the left border to the right border (the full `scan_range`).
For each bar `j` in that range:

**Bull check**: `low[j] <= bull_fvg_vtop[i]` AND `high[j] >= bull_fvg_bot[i]` for any active bull FVG `i`
**Bear check**: `high[j] >= bear_fvg_vbot[i]` AND `low[j] <= bear_fvg_top[i]` for any active bear FVG `i`

If no bar in the scan range satisfies the condition → level is NOT drawn.

### Why this works with current vtop/vbot
`vtop` at confirmation time = the lowest low that ever entered the bull FVG.
The bar that last updated `vtop` will have exactly `low[j] = vtop`, so `low[j] <= vtop` is true for it.
If that bar is within the scan range, the condition fires correctly.
If the only tap happened BEFORE the left border, then all bars in the scan range have `low[j] > vtop`,
and the condition correctly returns false.
