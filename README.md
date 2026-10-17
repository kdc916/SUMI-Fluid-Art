# SUMI Fluid Art — 墨流し

Two ways to paint: **流 Fluid** and **墨 Sumi (수묵/먹)**.

**[Try the web app](https://kdc916.github.io/SUMI-Fluid-Art/)** · Offline Android

## v0.5.0: Dual rendering modes

**Fluid / 유체:** Preserves the original colorful, swirling pigment simulation and mixing.

**Sumi / 수묵:** Adds a dedicated ink-wash deposition and renderer with high-density ink cores, pale layered wash, fiber-grain dry-brush gaps (kasure), edge pooling (tamari), and anisotropic capillary spreading (nijimi).

Switch styles without clearing your artwork. Existing ink stays on the canvas, while new input and rendering use the selected style.

### Controls

- Samsung Galaxy S Pen pressure (where supported), plus slow-thick / fast-thin brush response
- Stationary hold continuously deposits ink and spreads outwards
- Transparent **Water / 물** tool to dilute and push pigment, in both modes
- Adjustable drop size, flow and fade; pause, clear, dark paper, PNG save

### Technical structure

Single-file `index.html`; offline WebGL2 GLSL semi-Lagrangian fluid approximation with velocity projection, dye and stain layers; Canvas2D fallback. The Sumi path adds a separate shader display and anisotropic capillary pass; Fluid remains the existing path.

Open `index.html` in a browser or use GitHub Pages `main / (root)`. Android Studio project is in `android/`; its Gradle syncs the root HTML into the offline APK. CI lives in `.github/workflows/`.

**Testing:** Chromium Canvas2D automatic tests passed for drawing, switching without clearing, long-press growth, water dilution, and clearing. Android real-device GPU and S Pen pressure behavior still need testing. Reference images (including watermarked examples) are *not* bundled.

See `docs/HANDOFF_CUMULATIVE_v0.5.0.md` for technical changes and caveats.
