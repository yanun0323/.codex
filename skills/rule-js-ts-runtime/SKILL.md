---
name: rule-js-ts-runtime
description: Mandatory runtime/tooling rules for JavaScript/TypeScript projects - Bun as package manager + task runner, Node as default runtime, script hygiene, version pinning, and CI-safe commands.
metadata:
  short-description: Bun package manager + Node runtime rules for JS/TS.
---

# JS/TS Runtime & Tooling Rules (Bun + Node)

## When to Use
Load this skill for any JavaScript/TypeScript project work, including:
- Frontend (Vite, SolidJS, React, Vue, Svelte)
- SSR/Fullstack (SolidStart, Next.js, Nuxt, Remix, etc.)
- Tooling (Vitest/Jest, ESLint, Prettier, TS config, build scripts)

If any rule conflicts with explicit user instructions, follow the user instructions.
If any rule conflicts with rule-global, follow the higher-priority rule defined there.

---

## 1) Primary Policy (MANDATORY)

### 1.1 Bun is the package manager and task runner
- Use `bun install` for dependency installation.
- Use `bun run <script>` to execute `package.json` scripts.
- Prefer `bunx <pkg>` for one-off CLI executions (scaffolding, generators), ONLY when it does not change runtime behavior.

### 1.2 Node.js is the default runtime
- Assume Node.js executes dev/build/test tooling (Vite, TS, SSR servers) unless explicitly requested otherwise.
- Do NOT assume Bun runtime compatibility for SSR, server actions, or Node-specific APIs.

### 1.3 Avoid “Bun-as-runtime” by accident
- Do NOT invoke tools via `bun <tool>` (e.g., `bun vite`, `bun ts-node`, `bun node`).
- Do NOT write `package.json` scripts that call `bun` directly (unless user explicitly requests Bun runtime).

---

## 2) package.json Scripts Hygiene (STRICT)

### 2.1 Scripts MUST be runtime-agnostic
Scripts MUST call the tool directly:
- ✅ Allowed:
  - `"dev": "vite"`
  - `"build": "vite build"`
  - `"test": "vitest"`
  - `"lint": "eslint ."`
- ❌ Disallowed:
  - `"dev": "bun vite"`
  - `"build": "bun vite build"`
  - `"test": "bun vitest"`
  - `"lint": "bun eslint ."`

Rationale: `bun run <script>` will run these tools with the correct environment; embedding `bun` inside scripts locks behavior and frequently causes cross-environment drift (CI vs local).

### 2.2 Prefer `bun run` over tool-specific runners
- Prefer `bun run dev` over `vite dev`.
- Prefer `bun run test` over `vitest`.
This ensures consistent PATH resolution and lockfile usage.

---

## 3) Lockfile Policy (MANDATORY)

### 3.1 Bun lockfile is canonical
- `bun.lockb` is the canonical lockfile.
- Do NOT add or regenerate other lockfiles:
  - `package-lock.json`
  - `pnpm-lock.yaml`
  - `yarn.lock`

### 3.2 Do not mix package managers
- Do NOT run `npm install`, `pnpm install`, or `yarn` in this repo.
- If encountering a repo that already uses another lockfile, STOP and ask before migrating.

---

## 4) Version Pinning Policy (RECOMMENDED, OFTEN REQUIRED)

### 4.1 Pin Node version per repo
Use a project-level Node version strategy (one of the following, follow repo convention):
- Volta (`"volta": { "node": "..." }` in package.json)
- `.node-version` (asdf)
- `.nvmrc` (nvm)
- `engines.node` (package.json)

If no convention exists:
- Prefer Volta pinning for developer ergonomics.
- Otherwise set `engines.node` as a minimum.

### 4.2 Pin Bun version when supported
If the repo already pins Bun (e.g., `.bun-version`, tooling config), follow it.
If not pinned, do not introduce pinning unless requested.

---

## 5) CI-Safe Commands (MANDATORY WHEN EDITING CI DOCS)

When documenting or editing CI scripts:
- Install dependencies with:
  - `bun install --frozen-lockfile` (preferred)
- Run scripts with:
  - `bun run <script>`

Do NOT use `npm ci`, `pnpm i`, or `yarn install` unless explicitly requested.

---

## 6) Native Addons & Postinstall Scripts (CAUTION)

Bun intentionally changes the behavior of dependency lifecycle scripts in some contexts.
Therefore:
- If a dependency requires native compilation (node-gyp/N-API) or relies on postinstall hooks,
  assume Node-based execution is needed and DO NOT switch runtime to Bun.
- If installation/build fails, report:
  - failing package name(s)
  - error logs
  - whether it is a native addon/postinstall issue
  - recommended mitigation (use Node runtime, adjust dependency, or trustlist if repo policy allows)

Do NOT silently enable broad trust or bypass security constraints without explicit user approval.

---

## 7) SSR / Fullstack (DEFAULT TO NODE)

For SSR/fullstack projects (Next/SolidStart/Nuxt/Remix):
- Default runtime is Node.
- Do not rewrite server entrypoints to Bun or alter adapters to “make Bun work” unless explicitly requested.
- If user requests Bun runtime, provide:
  - compatibility risks
  - required config changes
  - clear rollback path

---

## 8) Verification Checklist (MINIMUM)

Before concluding:
- `bun install` succeeds (no new non-bun lockfiles introduced).
- `bun run dev` / `bun run build` / `bun run test` match repo expectations.
- `package.json` scripts remain runtime-agnostic (no embedded `bun ...`).
- If Node version pinning exists, it remains intact; if absent, note it as a recommendation.

---

## 9) When Uncertain

STOP and ASK if:
- The repo currently uses pnpm/yarn/npm and migration is implied.
- The project is SSR/fullstack and runtime assumptions might change deployment.
- A dependency requires native addons or postinstall hooks and policy is unclear.
