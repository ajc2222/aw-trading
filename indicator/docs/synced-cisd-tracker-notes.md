# Synced CISD Tracker — Dev Notes

File: `indicator/synced-manipulation.pine`

## What it does

Tracks CISD (Change in State of Delivery) potential across NQ, ES, YM simultaneously.
When any asset sweeps a structural low/high and has a valid bearish/bullish leg preceding it,
a label fires at the manipulation low/high. The label text updates in-place as more assets join
(e.g. "10:01 - ES" → "10:01 - ES + NQ"). Label disappears when all assets fail.

## Detection logic (`f_cisd`)

- `is_ll`: current bar makes a new low below `ta.lowest(low, sl)[1]` (sl-bar lookback), with sl-bar cooldown, and no existing pending bull setup
- `is_hh`: symmetric for highs
- On `is_ll`: look back up to 50 bars for first bearish bar (`close < open`), then walk that consecutive bearish leg to find highest open (`ho`). If `ho` found → `new_bull = true`, `pend_bull = true`, `bull_low = current low`
- Failure: if `pend_bull` and `low < bull_low` → reset `pend_bull = false`
- Returns `[new_bull, new_bear, pend_bull, pend_bear]`

## Label logic

- `bull_lbl` / `bear_lbl`: single `var label` per direction
- Created at first unlock bar/price, never moves — subsequent asset joins only call `label.set_text()`
- Deleted when `bear_failure` fires AND `bear_assets == ""` (all assets failed)
- `bear_failure` derived from state change: `not this_bear and this_bear[1]` etc.

## Key inputs

| Input | Default | Purpose |
|-------|---------|---------|
| Max Leg Length | 10 | Max consecutive bearish/bullish bars to scan for displacement leg |
| Swing Lookback | 20 | Bars for `ta.lowest/highest` sweep detection + cooldown length |

## Bugs fixed this session

1. **Labels not showing**: `pend_bull` stayed `true` forever → `bull_changed` only fired once off-screen. Fixed by returning `new_bull` (event) separately from `pend_bull` (state).
2. **Humongous green tint**: same root cause as above. `pend_bull` never reset.
3. **Label off-screen**: single tracking label was created at first ever detection (months back) and `label.set_text` updated it there. Fixed with `label.set_x`/`label.set_y`, later reverted to fixed-position (no move on asset joins).
4. **Label position moving on asset join**: `label.set_x/y` was called on every new asset unlock. Fixed by only setting position on first unlock (`na(bull_lbl)`), subsequent joins only call `label.set_text`.
5. **Too many labels**: `ta.lowest(low, 10)` fired on every trending bar. Fixed with larger lookback (20) + sl-bar cooldown (`bar_index - last_ll_bar >= sl`).
6. **Failed setup not deleting**: with tiny `swingLen`, every 2 bars a new `is_hh` reset `bear_high` to the new high — so failure condition `high > bear_high` was never satisfied. Fixed by guarding `is_ll`/`is_hh` with `not pend_bull`/`not pend_bear`.
7. **CE10272 "Undeclared identifier pend_bull"**: `var` declarations were after the `is_ll` line that referenced them. Fixed by moving all `var` declarations to top of function.

## Open issue (as of session end)

Nothing appearing after the CE10272 fix. Likely culprit: the `not pend_bull` guard combined with `pend_bull` starting `false` should be fine, but detection may not be firing on the user's current chart/timeframe. Debug approach from earlier session: add `bgcolor(this_bull ? green : ...)` and `plotshape(bull_unlock, ...)` to isolate whether the issue is in detection or label creation.

## Pine v6 gotchas hit this session

- `var` variables must be declared before any line that references them in a function
- `label.set_xy()` does NOT exist — use `label.set_x()` + `label.set_y()` separately
- `ta.pivotlow(low, sl, rightbars)` with `rightbars=5` adds 5-bar delay — sweeps can happen before pivot is confirmed, causing missed detections. `rightbars=1` is better.
- `request.security` with a function returning a 4-tuple works fine in Pine v6
- `barstate.isconfirmed` inside `request.security` correctly gates to confirmed bars of the requested security
