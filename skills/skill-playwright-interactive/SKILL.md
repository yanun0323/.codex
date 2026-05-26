---
name: "skill-playwright-interactive"
description: "Persistent browser and Electron interaction through `js_repl` for fast iterative UI debugging."
---

# Playwright Interactive Skill

Use persistent `js_repl` Playwright handles for iterative web/Electron debugging and QA.

## Preconditions

- `js_repl` must be enabled:

```toml
[features]
js_repl = true
```

Start a new session after enabling. Use from the target workspace. For now, use `sandbox_mode=danger-full-access`. Treat `js_repl_reset` as recovery only; it destroys handles.

One-time setup per workspace:

```bash
test -f package.json || npm init -y
npm install playwright
node -e "import('playwright').then(()=>console.log('playwright import ok')).catch(e=>{console.error(e);process.exit(1)})"
```

Install browser/Electron only as needed.

## QA Inventory First

Before testing, list coverage from: user requirements, implemented visible behavior, and final claims. Map every claim/control/state to functional and visual checks, expected evidence, and at least 2 off-happy-path scenarios. Update the inventory when exploration reveals new states.

## Bootstrap Once

```javascript
var chromium, electronLauncher, browser, context, page, mobileContext, mobilePage, electronApp, appWindow;
({ chromium, _electron: electronLauncher } = await import("playwright"));
```

Use `var` so later cells reuse handles. Keep cells short. If stale, set the handle to `undefined` and rerun the relevant cell; do not reset REPL unless broken.

## Web Helpers

```javascript
var resetWebHandles = () => { context = page = mobileContext = mobilePage = undefined; };
var ensureWebBrowser = async () => {
  if (browser && !browser.isConnected()) { browser = undefined; resetWebHandles(); }
  browser ??= await chromium.launch({ headless: false });
  return browser;
};
var reloadWebContexts = async () => {
  for (const c of [context, mobileContext]) if (c) for (const p of c.pages()) await p.reload({ waitUntil: "domcontentloaded" });
};
```

## Session Modes

- Default web: explicit viewport for reproducible QA/screenshots.
- Native-window web: separate pass for launch size, DPI, browser chrome, host-window issues.
- Electron: native-window behavior; check as-launched size before resizing.
- Switching viewport/native mode means new context/page.

Desktop web:

```javascript
var TARGET_URL = "http://127.0.0.1:3000";
if (page?.isClosed()) page = undefined;
await ensureWebBrowser();
context ??= await browser.newContext({ viewport: { width: 1600, height: 900 } });
page ??= await context.newPage();
await page.goto(TARGET_URL, { waitUntil: "domcontentloaded" });
```

Mobile web:

```javascript
var MOBILE_TARGET_URL = TARGET_URL ?? "http://127.0.0.1:3000";
if (mobilePage?.isClosed()) mobilePage = undefined;
await ensureWebBrowser();
mobileContext ??= await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
mobilePage ??= await mobileContext.newPage();
await mobilePage.goto(MOBILE_TARGET_URL, { waitUntil: "domcontentloaded" });
```

Electron:

```javascript
var ELECTRON_ENTRY = ".";
if (appWindow?.isClosed()) appWindow = undefined;
if (!appWindow && electronApp) { await electronApp.close().catch(()=>{}); electronApp = undefined; }
electronApp ??= await electronLauncher.launch({ args: [ELECTRON_ENTRY] });
appWindow ??= await electronApp.firstWindow();
```

## Iteration

- Renderer-only web: `await reloadWebContexts()`.
- Electron renderer-only: `await appWindow.reload({ waitUntil: "domcontentloaded" })`.
- Electron main/preload/startup change: close and relaunch Electron.
- Use real keyboard/mouse/touch for signoff; `evaluate` may inspect/stage but does not count.

## Functional QA

Run at least one end-to-end critical flow. Cover every visible control in the inventory, including reversible/stateful cycles. For animation/realtime, test real timing. After scripted checks, do 30-90 seconds of exploratory normal input; add any discovered state/control to inventory and test it.

## Visual QA

Separate from functional QA. Inspect initial viewport, required regions, every claimed state, meaningful post-interaction states, densest realistic state, and minimum/smaller realistic viewport. Check clipping, overflow, overlap, distortion, alignment, spacing, contrast, layering, readability, and motion states. Prefer viewport screenshots; use full-page only for debugging.

## Screenshots

For model-bound screenshots, emit CSS-pixel JPEGs. Use `page`/`mobilePage` for web and `appWindow` for Electron. Prefer:

```javascript
var emitJpeg = async bytes => codex.emitImage({ bytes, mimeType: "image/jpeg", detail: "original" });
var emitWebJpeg = async (surface, options = {}) => emitJpeg(await surface.screenshot({ type: "jpeg", quality: 85, scale: "css", ...options }));
```

Click returned coordinates directly for full captures; add `clip.x/y` for clipped captures. Native-window/Electron Retina captures may need CSS normalization; use renderer canvas resizing for web and `BrowserWindow.capturePage(...).resize(...)` for Electron.

## Signoff

Final answer should state functional coverage, visual coverage, viewport/window checks, exploratory pass, key negative confirmations, cleanup/kept-alive status, and any exclusions. Functional correctness, viewport fit, and visual quality must each pass independently.
