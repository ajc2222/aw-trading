# Spinning Gradient Border — Implementation Notes

## The Golden Rule
**The spinning gradient must always sit BEHIND the element it borders.**

The `::before` pseudo-element holds the gradient. The inner element (button, pill, card) must have:
- `position: relative`
- `z-index: 1`
- A **solid/opaque background** — semi-transparent backgrounds let the gradient bleed through the face of the element, not just its edge.

## Correct Pattern

```css
/* Wrapper */
.spin-wrap {
  position: relative;
  display: inline-flex;
  border-radius: 99px; /* match the inner element */
}
.spin-wrap::before {
  content: '';
  position: absolute;
  inset: -2px;               /* peeks out 2px at every edge */
  border-radius: 99px;       /* match wrapper */
  z-index: 0;                /* behind */
  animation: spin-grad 2.4s linear infinite;
  pointer-events: none;
}

/* Inner element — must be opaque and above */
.spin-wrap .btn {
  position: relative;
  z-index: 1;
  /* background must be opaque, e.g. #111114 for dark ghost buttons */
}

/* Gradient theme on the wrapper modifier */
.spin-gold::before {
  background: conic-gradient(from var(--spin-a), #FFD700, #FF8C00, #FFE566, #FF6B00, transparent 55%);
}
.spin-silver::before {
  background: conic-gradient(from var(--spin-a), #fff, #a0b4d0, #fff, #c8d8f0, transparent 55%);
}
```

## Common Mistake
Setting `background: rgba(...)` with any alpha < 1 on the inner element causes the gradient to show through the face of the button, not just the border ring. Always use a fully opaque background.

## Critical: stacking context
`position: relative` alone does NOT create a stacking context, so `z-index` on `::before` and the inner element won't stack relative to each other — the gradient ends up on top. Always add `isolation: isolate` to the wrapper:

```css
.firm-wrap { position: relative; isolation: isolate; }
/* now ::before z-index:0 and .firm z-index:1 are correctly ordered */
```

## Hover-only variant (for transparent/glass cards)
Glass cards have semi-transparent backgrounds, so z-index alone won't stop the gradient bleeding through the card face. Use **three layers**:

1. `::before` — full-size gradient (z-index: 0)
2. `::after` — solid opaque mask inset by the border width (z-index: 1), punches out the center so gradient only peeks at the 2px edge
3. `.card` — sits on top (z-index: 2), glass blends over the solid mask

```css
.firm-wrap { position: relative; border-radius: 20px; isolation: isolate; }
.firm-wrap::before { content:''; position:absolute; inset:0; border-radius:20px; z-index:0; animation:spin-grad 2.4s linear infinite; opacity:0; transition:opacity .35s; }
.firm-wrap:hover::before { opacity: 1; }
.firm-wrap.spin-silver::before { background: conic-gradient(from var(--spin-a), #fff, #a0b4d0, #fff, #c8d8f0, transparent 55%); }
.firm-wrap::after { content:''; position:absolute; inset:2px; border-radius:18px; background: var(--bg); z-index:1; pointer-events:none; }
.firm-wrap .firm { position:relative; z-index:2; }
```
