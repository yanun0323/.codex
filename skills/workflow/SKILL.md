---
name: workflow
description: Primary end-to-end workflow for repo changes - intake + TASK/SPEC docs + implementation (backend with optional UI) + review + fix, aligned with agents-* skills. Use only when the user explicitly asks to invoke or use the "workflow" skill.
metadata:
  short-description: End-to-end workflow (backend + optional UI).
---

# workflow

## Goals
- Provide a repeatable end-to-end change workflow that optimizes for **safety** (money/auth/data) while keeping documentation **proportional to risk**.
- Produce a closed loop: intake → plan/spec → implement → review → fix → verify.
- Keep TASK/SPEC lean by defaulting to per-change docs and treating root files as a short index.

## Definitions
### Change class
- **Trivial**: Non-executable, non-behavioral changes only (.comments/typos/formatting) with no production impact.
- **Small**: Behavior change limited to a single component, no API contract changes, and **no high-risk area touched** (see below). Can be fully covered by targeted tests.
- **Non-trivial**: Anything that is not Trivial/Small (cross-cutting changes, contract changes, infra changes, ambiguous impact, or any high-risk area).

### High-risk areas (Change Impact Matrix rows)
Treat the following as **high-risk rows**:
- Money/balances/orders
- Auth/permissions
- Migrations/data loss
- Concurrency/lifecycle
- API surface (when external clients depend on it)

If any high-risk row is **Yes** or **Ambiguous**, prefer **medium/high** risk until proven otherwise.

### Risk classification rubric (default)
- **Low**: Trivial, or Small with complete test coverage and no high-risk rows touched.
- **Medium**: Any API surface change without money/auth/data-loss risk, or multi-file changes with moderate blast radius.
- **High**: Any high-risk row = Yes (or cannot be confidently answered), or changes that can cause financial loss, data loss, privilege escalation, or widespread downtime.

## Skill integration
- Always load `agents-global`.
- Backend work: load `agents-go`.
- UI work: load `agents-solid` and `agents-ui`.
- Infra changes: load `agents-infra`.

## Step 0: Intake + Triage + Docs (TASK/SPEC)
### 0.1 Intake
- Restate the goal (1-2 sentences).
- List up to 3 assumptions if needed.
- Declare the **change class**: Trivial / Small / Non-trivial.
- Classify **risk**: low / medium / high (see rubric above).

### 0.2 Documentation gating (keep docs proportional + small)
- **Trivial**
  - No TASK/SPEC required.
  - Still include a verification note in the final output (e.g., “No runtime impact; verified by …”).
- **Small**
  - Create/update a **TASK doc**.
  - SPEC is optional unless a matrix-driven requirement applies (see 0.4).
- **Non-trivial**
  - Create/update a **TASK doc** and a **SPEC doc**.

Default locations (prevent root bloat):
- Prefer per-change files:
  - `.tasks/TASK-YYYY-MM-DD-<slug>.md`
  - `.specs/SPEC-YYYY-MM-DD-<slug>.md`
  - Create `.tasks/` and `.specs/` if missing.
- Keep root `TASK.md` / `SPEC.md` as a short index + rolling summary (<= ~20 lines) linking to the per-change docs.
- If the repo already standardizes on root TASK/SPEC, keep only the most recent sections in root and archive the rest (see 0.9).

### 0.3 TASK doc must include
- Title + date
- Change class + risk
- Goal, non-goals, assumptions
- Plan (checkbox list)
- Expected files/dirs
- Verification plan (commands + expected outcomes, manual checklist if needed)

### 0.4 SPEC doc must include (baseline)
- Problem
- Requirements (functional + non-functional)
- Domain rules / invariants
- Security / privacy notes
- Observability (request_id/logs)
- Rollout / rollback (if needed)
- Change Impact Matrix (required)

Additionally, include the following **only when applicable** (matrix-driven requirements):
- **API contract**: Required when `API surface = Yes`
- **Error codes + user-safe messages**: Required when `API surface = Yes` or `UI/Frontend = Yes`
- **Persistence/repository details**: Required when `Persistence/repository = Yes`
- **Migration / data safety plan**: Required when `Migrations/data loss = Yes`
- **Concurrency model**: Required when `Concurrency/lifecycle = Yes`
- **AuthZ matrix / permission notes**: Required when `Auth/permissions = Yes`
- **Perf/SLO notes**: Required when `Money/balances/orders = Yes` or `API surface = Yes` with high QPS

### 0.5 Change Impact Matrix (minimal table; required)
| Area                   | Change? | Files/Dirs | Risk | Notes |
| ---------------------- | ------- | ---------- | ---- | ----- |
| API surface            |         |            |      |       |
| Auth/permissions       |         |            |      |       |
| Money/balances/orders  |         |            |      |       |
| Domain logic           |         |            |      |       |
| Persistence/repository |         |            |      |       |
| Migrations/data loss   |         |            |      |       |
| Concurrency/lifecycle  |         |            |      |       |
| Config/env vars        |         |            |      |       |
| Infra (Docker/K8s)     |         |            |      |       |
| UI/Frontend            |         |            |      |       |
| i18n/copy              |         |            |      |       |
| Tests                  |         |            |      |       |
| Observability          |         |            |      |       |

### 0.6 STOP rule (blocking questions only)
If any **high-risk row** is **Yes** or **Ambiguous**, STOP and ask only blocking questions from this list:
- Does this change affect existing API behavior (including status codes / error codes / semantics)?
- Do we need backward compatibility (old clients/workers) or versioning?
- For money/order flows: what is the idempotency key and replay behavior?
- For migrations: can we safely roll forward and roll back? What is the rollback plan?
- For auth: what is the permission boundary and how is it enforced?
- For concurrency: what are the lifecycle guarantees and race conditions we must prevent?
- Do we need a feature flag or staged rollout? What is the rollout/rollback trigger?
- What are the minimum observability signals required (request_id, audit trail, key logs/metrics)?

### 0.7 Verification minimum bar (unless repo lacks these tools)
Verification plan should include, at minimum:
- Backend: `go test ./...` (or the repo’s test command) + any relevant targeted tests
- If touching API: at least one contract verification (integration test, golden test, or curl example with expected output)
- If touching persistence/migrations: migration dry-run / schema validation (repo-specific)
- If touching money/orders: at least one invariant-focused test (e.g., non-negative balances, idempotent replay, no double-spend)
- If touching auth: at least one permission-focused test (deny-by-default where applicable)

If a minimum item is not possible, explicitly state why (e.g., “no test harness present”) and propose a mitigation.

### 0.8 Docs-only mode
If the user only asks for TASK/SPEC, perform Step 0 and stop.

### 0.9 Archival policy (avoid infinite growth)
If root TASK/SPEC is used and grows beyond one of these thresholds:
- > 10 dated sections, OR
- > ~400 lines
Then archive older sections to `.history/<TASK|SPEC>-YYYY-MM.md` or convert them into per-change docs under `.tasks/` and `.specs/`. Keep only the most recent sections + links in root.

## Step 1: Implement (backend)
- Follow `agents-go` rules and layering.
- Keep diffs minimal; no drive-by refactors.
- Add tests per risk level (`agents-global`).

Additional safety requirements (when applicable):
- If `API surface = Yes`: preserve backward compatibility or provide versioning/migration path.
- If `Money/balances/orders = Yes`: enforce idempotency and invariants in code + tests; avoid non-atomic updates.
- If `Migrations/data loss = Yes`: implement forward-safe migrations; document rollback and data backfill strategy if needed.
- If `Auth/permissions = Yes`: default-deny where possible; ensure authorization checks are server-side and covered by tests.

## Step 2: UI (optional)
UI is applicable if:
- the repo has a frontend workspace (package.json + src/ or Vite/Solid config), or
- the user explicitly requests UI changes.

If UI is applicable:
- Follow `agents-solid` and `agents-ui`.
- Implement loading, empty, error, success states.
- Centralize copy:
  - Use **English semantic keys** (e.g., `order.cancel.success`).
  - Use `zh-TW` values by default; if the repo supports `en-US`, keep key parity.

If UI is not applicable:
- State: "UI step skipped: no frontend workspace detected or not requested."

## Step 3: Review (Critic)
- Do NOT modify code.
- Output issues with file refs and fix suggestions using the following severity rubric:
  - **P0**: correctness/security/data loss/financial loss, broken build/tests, privilege escalation
  - **P1**: reliability/perf regressions, missing observability, insufficient tests for medium/high risk
  - **P2**: maintainability/consistency/style, minor refactors, naming/structure cleanup

Recommended output shape:
- Summary (1-3 bullets)
- Issue list (ordered by fix priority)
  - `Severity`: P0/P1/P2
  - `Location`: file:line or file path
  - `What/Why`: short description + impact
  - `Fix suggestion`: concrete minimal fix
  - `Fix order`: integer (1..N)

## Step 4: Fix + Verify
- Apply minimal diffs.
- Re-run verification commands.
- Provide output format per `agents-global`.

## Optional: Automation hooks (recommended for teams)
- Mirror Change Impact Matrix into PR template checklist.
- CI gates:
  - If matrix marks `Migrations/data loss = Yes`, require migration plan section in SPEC.
  - If matrix marks `Money/balances/orders = Yes`, require at least one invariant test file change.
  - If matrix marks `API surface = Yes`, require contract test update or explicit compatibility note.

## Output
When code changes are involved, follow `agents-global` output format.
