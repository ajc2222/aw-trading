# Design System

A domain-agnostic design system extracted from the AW Trading site (`index.html`): dark glass surfaces, one accent color, an Archivo/IBM Plex Mono type pairing, and a small set of motion rules. Everything below is generalized so it drops into an education platform, a social app, or a dashboard without renaming a thing.

**Files this doc mirrors** (in `docs/design-system/`): `tokens.css`, `motion.css`, `components.css`, `patterns.css`, `index.html` (live reference page).

To re-skin for a new brand: change `--accent` (and `--accent-ink` if you need dark text on it) in `tokens.css`. Every glow, badge, and focus ring derives from those.

---

## 1. Foundations (`tokens.css`)

### Color

| Token | Value | Use |
|---|---|---|
| `--bg` | `#070709` | Page background |
| `--panel` | `#0c0c10` | Base surface |
| `--panel-2` | `#111116` | Nested surface (avatars, inputs) |
| `--text` | `#F5F6F8` | Primary text |
| `--text-muted` | `#9298A6` | Secondary text |
| `--text-dim` | `#6A6F7C` | Tertiary / timestamps |
| `--line` | `rgba(255,255,255,.12)` | Default border |
| `--line-strong` | `rgba(255,255,255,.26)` | Emphasized border |
| `--accent` | `#2E6BFF` | The one brand color — change this to re-skin |
| `--accent-glow` | `rgba(46,107,255,.4)` | Glow/shadow paired with accent |
| `--accent-ink` | `#ffffff` | Text placed on top of solid `--accent` |
| `--success` | `#2ECC71` | Positive status |
| `--warning` | `#F5A623` | Caution status |
| `--danger` | `#FF4D4F` | Negative / destructive status |
| `--glass-hi` / `--glass-lo` | `rgba(255,255,255,.09)` / `.035` | Glass gradient stops |

A light theme override is included, swapping `--bg/--panel/--text/--line/--glass-*` while keeping the accent formulas identical:

```css
:root[data-theme="light"]{
  --bg:#F5F6F8; --panel:#FFFFFF; --panel-2:#F0F1F5;
  --text:#0A0A0B; --text-muted:#4B5160; --text-dim:#7A8090;
  --line:rgba(10,10,15,.10); --line-strong:rgba(10,10,15,.22);
  --glass-hi:rgba(10,10,15,.04); --glass-lo:rgba(10,10,15,.015);
}
```

### Type

- **Display**: `'Archivo', sans-serif` — headings, buttons, brand.
- **Mono**: `'IBM Plex Mono', monospace` — eyebrows, timestamps, data, badges.
- Scale: `--text-xs .72rem` → `--text-3xl clamp(2.4rem,5.4vw,3.9rem)` (fluid, see `tokens.css` for all steps).

### Spacing & radius

- Spacing scale (4px base): `--space-1` (4px) through `--space-8` (64px).
- Radius scale: `--radius-sm` 8px, `--radius-md` 14px, `--radius-lg` 22px, `--radius-pill` 99px.

### The glass recipe (the one signature surface)

```css
.glass{
  background:linear-gradient(160deg,var(--glass-hi),var(--glass-lo) 50%);
  backdrop-filter:blur(18px) saturate(1.3);
  -webkit-backdrop-filter:blur(18px) saturate(1.3);
  border:1px solid var(--line);
  box-shadow:var(--shadow-inset-hi),var(--shadow-inset-lo),var(--shadow-drop);
}
```

### Ambient background effects

- `.liquid` + `.blob` — soft blurred color blobs drifting behind content (`motion-drift-a/b/c` in `motion.css`).
- `.grain` — subtle noise texture overlay.
- `.grid-overlay` — faint graph-paper grid, masked to fade at the edges.

---

## 2. Motion (`motion.css`)

Named by **intent**, not by the component they first appeared on — any component can borrow any effect.

| Class / keyframe | Effect | Typical use |
|---|---|---|
| `motion-drift-a/b/c` | Slow ambient float | Background blobs, decorative shapes |
| `rim-pulse` (used via `.glow-ring`) | Pulsing neon border | The one CTA that matters on screen |
| `sheen` (used via `.logo-mark`) | Light bar sweeping across a shape, looping | Brand chips, logo marks |
| `card-sweep` (used via `.card-sweep`) | Diagonal shimmer on hover | Testimonials, feature spotlights |
| `blink` (used via `.dot-live`) | Opacity pulse | "Live" / "online now" status dots |
| `underline-reveal` (used via `.motion-underline`) | Underline draws in on load | One emphasized word in a heading |
| `.motion-lift` | Hover: translateY(-4px) | Cards |
| `.motion-press` | Hover: translateY(-2px) | Buttons |

All motion respects `prefers-reduced-motion: reduce` globally (defined in `tokens.css`), collapsing durations to near-zero and dropping ambient opacity.

---

## 3. Components (`components.css`)

### Buttons

```html
<div class="glow-ring"><button class="btn btn-primary">Primary <span class="arrow">→</span></button></div>
<button class="btn btn-accent">Accent</button>
<button class="btn btn-ghost">Ghost</button>
<button class="btn btn-primary btn-small">Small</button>
```

- **`.btn-primary`** — elevated light surface. Use for **one** main action per view.
- **`.btn-accent`** — solid accent fill. Secondary emphasis, or on light backgrounds.
- **`.btn-ghost`** — glass outline. Secondary/tertiary actions.
- **`.glow-ring`** — wraps a single `.btn` to mark it as *the* call to action on the page (pulsing border).
- `.btn:disabled` drops opacity and disables pointer events automatically.

### Badges & status

```html
<span class="badge badge-accent">NEW</span>
<span class="badge badge-success">ONLINE</span>
<span class="badge badge-warning">PENDING</span>
<span class="badge badge-danger">URGENT</span>
<span class="dot dot-live"></span> live now
```

### Cards

- `.card` — base padded, rounded, overflow-hidden container.
- `.card-hover` — lift + accent-glow shadow on hover.
- `.card-sweep` — adds the diagonal shimmer sweep on hover (pair sparingly — testimonials, spotlighted items).

### Avatars

`.avatar` + size modifier `.avatar-sm` / `.avatar-md` / `.avatar-lg` — circular, initials-based, `--panel-2` background.

### Nav

`.nav` is a sticky, blurred glass bar; `.nav-links` collapses under 900px (pair with your own mobile menu toggle).

### Forms

Inputs, selects, and textareas share one focus treatment: border turns `--accent`, plus a soft `--accent-glow` ring.

**Reveal-gate pattern** — for gated forms or paywalled previews: content blurs behind `.reveal-gate-content.locked`, with a `.reveal-gate-overlay` lock message on top. A CTA click removes `.locked` and the overlay's `.hidden` class is added.

### Accordion

`.accordion` + native `<details>/<summary>` — a `+` marker rotates 45° into an `×` on open. Works for FAQs, course syllabi, or comment threads.

### Modal / lightbox

`.modal` (fixed, dark scrim) + `.modal.active` to show. `.modal-lightbox` sets `cursor: zoom-out` for image lightboxes.

### Section headers

`.section` / `.section-panel` (bordered variant) for page rhythm; `.sec-head` for the eyebrow + heading + description block that opens each section.

---

## 4. Composite patterns (`patterns.css`)

Generalized from the trading site's specific widgets:

| Pattern | Generalized from | Reuse as |
|---|---|---|
| `.chat-panel` | Discord widget | Any live-community panel or DM UI |
| `.scroll-track` | Certificate marquee | Logo strips, testimonial carousels, story rails |
| `.leaderboard` | Prop-firm podium | Rankings, gamified badges, top-contributor rows |
| `.stat-tile` / `.stat-row` | "6,600+ members" mini-tabs | Dashboard KPIs, quick-glance metrics |
| `.bar-chart` | Indicator candles | Any small inline chart — progress, activity, price |
| `.feature-row` | Indicator feature list | Plan features, course modules |

### Scroll track

Duplicate the track's children once (so there's a clean loop point), then drive position from scroll with the framework-agnostic JS included as a comment in `patterns.css`:

```js
function initScrollTrack(track, direction){
  if(!track) return;
  let target=0, current=0, lastY=window.scrollY, half=track.scrollWidth/2;
  window.addEventListener('resize', ()=>{ half = track.scrollWidth/2; }, {passive:true});
  (function loop(){
    const y=window.scrollY;
    target += direction*(y-lastY); lastY=y;
    current += (target-current)*0.08;
    const pos = ((current % half) + half) % half;
    track.style.transform = `translateX(${-pos}px)`;
    requestAnimationFrame(loop);
  })();
}
initScrollTrack(trackA, 1);   // drifts one way on scroll
initScrollTrack(trackB, -1);  // opposite direction reads as intentional, not random
```

### Chat panel

Three-column grid (`icon rail` / `channel list` / `chat body`) that collapses to two columns under 560px (hiding the channel list). Swap "channels" for DM threads, course modules, or subreddit-style categories — the structure is domain-neutral.

### Leaderboard

`.rank-tile.rank-1/2/3` — rank 1 is visually larger with an accent-colored ring; ranks 2/3 sit lower with a neutral badge. Works for prop-firm rankings, course leaderboards, or top-poster lists.

---

## 5. Applying it to a new domain

No new components needed — recombine the pieces above.

**Education platform course card:**
```html
<div class="glass card">
  <div class="eyebrow">Course</div>
  <h3>Intro to Data Structures</h3>
  <div class="feature-row"><div class="feature-icon">✓</div><span>12 modules · self-paced</span></div>
  <div class="feature-row"><div class="feature-icon">✓</div><span>Certificate on completion</span></div>
  <div class="glow-ring"><button class="btn btn-primary btn-small">Enroll free <span class="arrow">→</span></button></div>
</div>
```

**Social platform post card:**
```html
<div class="glass card card-hover">
  <div style="display:flex;align-items:center;gap:10px">
    <div class="avatar avatar-md">MK</div>
    <div><b>maya.k</b><span class="text-muted">2h ago</span></div>
    <span class="badge badge-accent">TRENDING</span>
  </div>
  <p>Shipped the new onboarding flow today — feels so much cleaner 🎉</p>
  <div class="font-mono text-muted"><span>♥ 248</span> <span>💬 31</span></div>
</div>
```

---

## 6. Live reference

`docs/design-system/index.html` renders every token, component, and pattern above with real markup — open it in a browser (or view the published artifact) to see hover states, the accordion, and the chat/leaderboard patterns interactively. The PDF export of that page is static and loses hover/interactive states; this markdown file and the HTML reference are the source of truth.
