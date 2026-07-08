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

### Protected Low (bull)
The absolute lowest wick across ALL bars between left border and right border (inclusive).
Candle type does not matter — wicks and bodies both count.
Line drawn from that bar's bar_index to the confirmation bar.

### Protected High (bear, mirror)
The absolute highest wick between left and right borders.

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
