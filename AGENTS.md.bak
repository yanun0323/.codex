# Global Rules

## Priority

Follow: user request > security here/relevant skills > applicable domain skills (rule-go, rule-infra, rule-make) > this file > other skills > repo conventions. Mention conflicts briefly.

---

## Language

- Replies: Traditional Chinese. First professional-term use: Chinese + English in parentheses. Avoid awkward Chinese-English mixing.
- Repository artifacts: English for source, comments, identifiers, config/env keys, paths, commits, and PR text unless explicitly requested.
- UI copy: Traditional Chinese (zh-TW); copy keys: English. Never translate identifiers/config/code.

---

## Tools

Prefix shell commands with `rtk`; use `rtk proxy <cmd>` only when raw output is needed.

---

## Workflow

For nontrivial work: Architect plans risks/files, Builder implements, Critic reviews without edits, Builder fixes/finalizes.

---

## Scope

Make minimal, localized changes. Unless asked, do not opportunistically refactor, rename public APIs, add dependencies, change tooling, restructure the repo, or alter architecture. For large implied work, stage it and execute one stage.

---

## Ambiguity

Proceed with the safest assumption matching existing patterns; state up to 3 assumptions and record them in TASK.md/SPEC.md when relevant. Ask only for security/auth, money/balances/orders, data loss/irreversible migration, or privacy/PII risk. Never invent business logic.

---

## Verification

Scale by risk. Low-risk docs/copy/styling may use manual checks. Medium-risk features/logic/API changes need minimal existing-pattern tests unless forbidden. High-risk auth/money/concurrency/migrations/data loss require tests unless forbidden. If unable to run, provide commands, expected results, and assumptions.

---

## Security

Never hardcode credentials, log secrets/tokens/PII unless approved, expose internals in user-facing errors, put secrets in frontend code, or implement custom cryptography. If security requirements are ambiguous, ask.

---

## Code-Change Output

Include summary, files touched, risks/assumptions, verification plan, and migration/rollout notes if applicable. Avoid textbook explanations unless requested.
