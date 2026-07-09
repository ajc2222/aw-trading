# AW Trading — Framework Notes
> Reference for content accuracy. Updated as we build carousels and scripts.

---

## Instrument + Session
- **Instrument:** NQ (Nasdaq futures)
- **Session:** NY Open (7am–10am EST)

---

## Bias Framework (4H → 1H → 15m)
Bias is determined by **multiple inputs together** — not any single factor alone.

1. **PD Arrays (4H):** Are they being respected or disrespected?
   - Respecting = institutional interest still present → trade into it
   - Disrespecting = level invalidated → don't fade it
2. **Open DOL:** Where is price being delivered? (See DOL section below)
   - DOL helps inform direction — but is NOT the sole basis for bias
3. **Path of least resistance:** Trade AWAY from manipulation (high resistance) and TOWARD failure swings / open space (low resistance)

**Bias = all three inputs aligned.** If they conflict, wait.

---

## Draw on Liquidity (DOL)
- **Open DOL** = price hasn't reached the level yet (untouched = still a magnet)
- **Taken DOL** = price has reached it — no longer a target, move on

### Valid DOL Types on NQ

**Structural:**
- Swing highs / swing lows
- Equal highs / equal lows (stop cluster)
- Relative equal highs / lows
- Failure swings (weak-side swing that failed to make a new high/low)

**Time-based:**
- Previous Day High / Low
- Previous Week High / Low
- Previous Month High / Low
- Session High / Low
- High of Day / Low of Day
- NDOG (New Day Opening Gap)
- NWOG (New Week Opening Gap)

### Prioritization
- Context-dependent, but **HTF DOL takes priority** over intraday DOL
- HTF + intraday DOL alignment = high conviction
- HTF vs. intraday conflict = wait, don't force

---

## PD Arrays (4H reference)
- Premium/Discount Arrays: FVGs, order blocks, voids, etc.
- Check whether price is **respecting** (institutional interest) or **disrespecting** (level dead)
- Used as step 1 in the 4H bias read
- "Respecting" = price reacts to the level → institutional order flow still present, trade into it
- "Disrespecting" = price blows through cleanly → level is dead, don't fade it

---

## Entry Trigger: CISD (Change in State of Delivery)
- **When:** After 2+ correlated assets have manipulated an intraday high/low (ITH/ITL) OR mitigated an HTF FVG
- **What it is:** Price shifts from bearish delivery to bullish (or vice versa) on the execution timeframe
- **Multi-asset filter:** NQ alone is not enough — need 2+ correlated assets (e.g. NQ + ES) to confirm the same manipulation before looking for CISD
- No CISD = no entry, regardless of how good the setup looks

---

## Full Setup Process (step by step, as AJ described it)

This is the exact sequence. Each step is a filter — if it doesn't pass, no trade.

1. **4H PD Arrays** — Is price at a key PD array? Is it respecting or disrespecting?
2. **Open DOL** — Where is price being delivered toward? Is there an open, untouched draw above or below?
3. **Path of least resistance** — Is there open space (low resistance) toward the DOL, or is price fighting manipulation zones (high resistance)? Trade toward the easy path.
4. **2+ Asset Confirmation** — Do NQ AND at least one other correlated asset (e.g. ES, YM) both show the same manipulation (stop raid on same ITH/ITL or same HTF FVG mitigation)?
5. **CISD on execution TF** — Only after step 4 is confirmed, look for the Change in State of Delivery. This is the actual entry signal.

> "You need all of these aligning. If any one of them is missing, you sit on your hands."

---

## Key Language / How AJ Explains These Concepts

These are phrasings AJ uses naturally — use these in content, not textbook definitions.

- **DOL:** "Price is always being delivered somewhere. The draw is where it's going next — the untouched level it's being pulled toward like a magnet."
- **Open vs Taken:** "If price has already been there, it's no longer a draw. The magnet is gone. Move on."
- **Bias:** "Bias isn't just one thing. I'm looking at where price is relative to PD arrays, what the closest open draw is, and whether there's room to run. All three have to agree."
- **Path of least resistance:** "I'm not fighting. I trade toward open space, away from wherever the manipulation happened."
- **Multi-asset filter:** "If NQ is sweeping a high but ES isn't doing the same thing, I'm not touching it. I need both."
- **CISD:** "Once I've got multi-asset confirmation, I wait for price to flip on the execution timeframe. That flip is my entry signal — the CISD."
- **No trade:** "If I can't identify a clear open DOL, or the assets aren't agreeing, or there's no CISD — I don't trade. The best trade is sometimes no trade."

---

## Common Misconceptions to Avoid in Content

These corrections came up when reviewing carousel drafts — don't repeat these errors:

1. **DOL is NOT the whole bias.** DOL is one input. Bias = PD arrays + DOL + path of least resistance, all aligned. Never write "find the nearest DOL = your bias."
2. **Generic ICT steps don't reflect AJ's actual process.** His setup isn't "market structure → liquidity → order block → confirmation" in the generic sense. It's the specific 5-step sequence above.
3. **CISD is not just a market structure shift.** It requires multi-asset confirmation first. Don't present it as a standalone signal.
4. **HTF DOL > intraday DOL**, but this is context-dependent — don't present it as a rigid rule without nuance.

---

## Carousel Content Notes

| # | Title | Key accuracy note |
|---|-------|-------------------|
| 1 | 3 ICT Terms | Generic intro — Liquidity, Order Blocks, Market Structure. Intentionally broad (Week 1 hook content). |
| 2 | How I Find My NQ Setups | Full 5-step process: 4H PD Arrays → Open DOL → Low Resistance → 2+ Asset Confirm → CISD. Written to AJ's actual method. |
| 3 | What is a Draw on Liquidity | DOL is ONE input into bias, not the whole bias. Slides 6+7 revised to reflect this nuance explicitly. |
| 4 | PD Arrays | TBD — ask questions before writing. |
