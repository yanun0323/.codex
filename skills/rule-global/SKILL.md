---
name: rule-global
description: Always load this skill for any task. Global rules for all coding tasks in this repo - priority, language policy, scope, ambiguity handling, verification, security, output format, and which domain skills to load.
---

# Global Rules for This Repository


## 0) Rule Priority (Highest to Lowest)

1. Explicit user instructions in the current request
2. Security rules (in this skill + relevant domain skills)
3. Domain skills, when applicable:
  - rule-go
  - rule-solid
  - rule-ui
  - rule-infra
  - rule-js-ts-runtime
  - rule-make
4. This skill
5. Other skills
6. Existing repository conventions (when not in conflict)

When rules conflict, follow the higher priority rule and explain the conflict briefly.

---

## 1) Language Policy (STRICT)

### 1.1 Chat Responses
- Always respond in Traditional Chinese.

### 1.2 Repository Artifacts
Repository artifacts MUST be written in English, including:
- Source code
- Code comments
- Identifiers, API field names, config keys, env var names
- File/folder names
- Commit messages, PR titles/descriptions (unless user explicitly asks otherwise)

### 1.3 User-Facing Product Copy
- User-facing UI copy MUST be Traditional Chinese (zh-TW).
- Copy keys MUST be English.

NEVER translate identifiers/config keys/code into Chinese.

---

## 2) Default Agent Workflow (Recommended)

Use separated roles to avoid self-justification:
- Architect: plan + risk + file list
- Builder: implement incrementally
- Critic: review strictly, list issues, no code changes
- Builder: fix issues + finalize

---

## 3) Scope and Change Policy (STRICT)

- Prefer minimal, localized changes.
- Do not perform drive-by refactors.
- Do not rename exported/public APIs unless explicitly requested.
- Do not introduce new dependencies without explicit approval.
- Do not change build tooling, repository structure, or architectural patterns unless instructed.
- If a request implies large changes, propose a staged plan and execute one stage only.

---

## 4) Ambiguity Handling (ASSUME-THEN-CONFIRM)

Default behavior is to proceed safely, not to stall.

If requirements are unclear:
- List up to 3 explicit assumptions.
- Proceed with the safest assumption consistent with the existing codebase patterns.
- Mark assumptions clearly in the response and (if applicable) in TASK.md/SPEC.md.

STOP and ASK only when a wrong decision could cause:
- security/auth boundary issues
- money/balance/order correctness issues
- data loss or irreversible migrations
- privacy/PII leakage

Never invent business logic.

---

## 5) Verification Policy (RISK-BASED)

### 5.1 Risk Levels
- Low risk: docs/copy/styling, refactor with no behavior change
- Medium risk: new feature, non-trivial logic, API behavior change
- High risk: auth/permissions, money/balances/orders, concurrency, migrations, data-loss risk

### 5.2 Requirements
- Low risk:
  - Tests optional
  - Provide manual verification checklist

- Medium risk:
  - Add minimal tests following existing patterns (unless user forbids tests)
  - Provide commands to run (or CI jobs) and expected outcomes

- High risk:
  - Tests REQUIRED (unless user explicitly forbids)
  - Provide exact verification commands and a rollback strategy (if applicable)

If execution is not possible in the current environment, still provide:
- the commands to run
- the expected output / success criteria
- key assumptions about runtime behavior

---

## 6) Security Baseline (HARD)

- Never hardcode secrets or credentials.
- Never log secrets/tokens/PII (unless explicitly approved).
- User-facing errors must not expose internal details (stack traces, SQL, hostnames).
- Frontend must never receive or store secrets.
- Do not implement custom cryptography. Use established libraries/patterns.
- If security requirements are ambiguous, STOP and ASK.

---

## 7) Output Format (When Code Changes Are Involved)

When proposing or delivering code changes, include:

1) Summary (what changed and why)
2) Files touched (bulleted list)
3) Risks / assumptions (explicit)
4) Verification plan:
   - commands to run (tests/linters/build)
   - manual verification checklist (if needed)
5) Migration/rollout notes (if applicable)

Avoid long textbook explanations unless requested.

---

## 8) Domain Skills to Load (Before Making Changes)

Load the relevant domain skills before making changes:
- Backend (Go + Echo): rule-go
- Frontend (SolidJS): rule-solid
- Frontend UI shard-solid enforcement: rule-solid-shard
- UI layer rules: rule-ui
- Infra/container/config: rule-infra
