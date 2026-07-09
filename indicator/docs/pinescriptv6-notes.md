# Pine Script v6 — Working Notes
Source: https://github.com/codenamedevan/pinescriptv6

---

## Execution Model

- Script runs **once per bar**, left to right across history, then once per tick on the live bar.
- On historical bars `barstate.isconfirmed = true`; on the unconfirmed live bar it is `false` and the bar re-executes on every tick until it closes.
- `var` variables persist across bars. Without `var`, a variable resets every bar.
- `varip` fields on UDTs persist intra-bar (survive rollback on tick updates).

---

## Timeframe / Period Detection

```pine
// CORRECT — fires exactly once on the first bar of each new period
bool new_day = timeframe.change("1D")

// WRONG — ta.change returns 0 (not na) when period hasn't changed; fires every bar
bool new_day = not na(ta.change(time("1D")))  // ← BUG
```

---

## request.security — Pitfalls

- `request.security(sym, "1D", high[1])` returns the PRICE of the previous completed daily bar.
- **CRITICAL**: this price is from the higher-timeframe series and is NOT guaranteed to align with any specific intraday bar's `bar_index`.
- **Never mix** `request.security` prices with manually tracked `bar_index` positions for the same level — they come from different execution contexts and will diverge.
- For PDH/PDL: track both the price AND the bar position manually in the intraday series so they're always in sync.

```pine
// BAD — price from security, bar from manual tracking → misaligned
float pd_high = request.security(syminfo.tickerid, "1D", high[1])
var int pd_h_bar = na  // tracked separately → desync!

// GOOD — everything from the same intraday tracking
var float pd_high = na
var int   pd_h_bar = na
// update both from the same source on new_day
```

---

## line.new() — Signature (v6)

```pine
// Two overloads — max 10 args each. No text parameters on lines.
line.new(first_point, second_point, xloc, extend, color, style, width, force_overlay)
line.new(x1, y1, x2, y2, xloc, extend, color, style, width, force_overlay)
```

- **No `text`, `text_color`, `text_size` params exist on `line.new()`** — use a separate `label` for text on a line.
- Minimum x-coordinate with `xloc.bar_index`: `bar_index - 10000`. For longer lookbacks use `xloc.bar_time`.
- `extend.none` (default) — line only renders between x1 and x2.

---

## label.new() — Best Practices for Price-Level Text

To show text sitting ON a horizontal line at a price level:

```pine
label.new(
    x         = bar_index,      // right endpoint of the line
    y         = price,
    text      = "Asia H.",
    yloc      = yloc.price,     // anchor y at exact price
    style     = label.style_none, // no box/arrow, pure text
    textcolor = col,
    size      = size.small,
    textalign = text.align_right  // text body extends LEFT of x, ending at x
)
```

- `text.align_right` → right-edge of text is at `x`, body extends left onto the line.
- `text.align_left`  → left-edge of text is at `x`, body extends right OFF the line.
- `label.style_none` + `yloc.price` = no box, text centered vertically at the price.

---

## UDT Objects — Reference Semantics

```pine
type Foo
    int val

var arr = array.new<Foo>()
array.push(arr, Foo.new(1))

f = arr.get(0)   // f is a REFERENCE to the object in the array
f.val := 99      // mutates the actual array element — persists!
```

- UDT objects are **always by reference** (like pointers).
- `array.get(arr, i)` returns a reference — mutations via that reference update the array element.
- Primitives (`int`, `float`, `bool`) inside UDT fields are value types but accessed via the object reference, so assigning `obj.field := x` DOES persist.

---

## for Loop Guard with Arrays

```pine
// WRONG — when array is empty, size()-1 = -1 and the loop runs once
for i = 0 to array.size(arr) - 1
    ...

// CORRECT — guard with explicit size check
int n = array.size(arr)
if n > 0
    for i = 0 to n - 1
        ...
```

---

## Session Detection

```pine
bool in_session = not na(time(timeframe.period, "0000-0900", "UTC"))
bool sess_end   = not in_session and in_session[1]  // first bar AFTER session
bool sess_start = in_session and not in_session[1]  // first bar OF session
```

- `time()` returns `na` when the current bar is outside the session → use `not na(...)` to detect membership.
- Session end fires on the first bar AFTER the session closes (not the last bar inside).

---

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| CE10115 — too many args to line.new() | Passing text/text_color/etc. to line.new() | Use separate label |
| CE10120 — line.new has no 'text' argument | Text is not a line parameter in v6 | Use separate label |
| CE10271 — line.set_text_color doesn't exist | Function doesn't exist in v6 | Use label |
| Array index out of bounds | `for i = 0 to size-1` when size=0 runs once | Add `if n > 0` guard |
| PDH/PDL draws at wrong bar | Mixing request.security price with manual bar_index | Use only manual tracking |
