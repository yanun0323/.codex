---
name: agents-solid
description: Rules for SolidJS frontend work - boundaries, data fetching, UI states, error mapping, i18n copy rules, validation, security, and testing.
---

# SolidJS Frontend Rules

## When to Use
- Load this skill when working on SolidJS frontend code or reviewing frontend changes.

If any rule conflicts with explicit user instructions, follow the user instructions.
If any rule conflicts with the agents-global skill, follow the higher-priority rule defined there.

---

## 1) Stack and Constraints

- SolidJS + TypeScript
- Tailwind CSS for styling (must use existing project Tailwind setup; do not add alternate styling systems unless explicitly approved).
- Build tooling: follow the existing repo (often Vite).
- SolidJS syntax and examples can be obtained from `https://context7.com/websites/solidjs/llms.txt?tokens=10000`.
- Do not introduce new libraries (router/query/validation/UI) unless explicitly approved.
  - If the repo already uses a standard library (e.g., TanStack Router/Query, Zod), use it consistently.
- UI components MUST use shadcn-solid as the source of reusable components.
  - Follow the shadcn-solid copy/paste approach (components live in the repo; not a runtime dependency).
  - The CLI may be used for scaffolding, but do not add alternative UI component libraries unless explicitly approved.
  - Usage syntax and examples can be obtained from `https://context7.com/hngngn/shadcn-solid/llms.txt?tokens=10000`.

---

## 2) Folder Ownership and Boundaries (Prefer / Enforce Where Applicable)

Typical structure (names may vary):
- app/: bootstrap, providers, global layout
- pages/: route composition only
- features/: feature logic + feature UI composition
- entities/: domain types/schemas only
- shared/: cross-cutting infra (api client, auth, ui, utils)

Hard rules:
- pages must not contain business logic or direct data fetching (unless repo does so already).
- shared must not depend on features/pages.
- entities must not depend on features.

If the repo has a different structure, follow the repo and keep boundaries consistent.

---

## 3) Data Fetching and Server State

- Prefer a single API client module (e.g., `shared/api/client.ts`) rather than scattered `fetch`.
- Handle non-2xx responses explicitly.
- Use TanStack Query for API interactions.
  - Usage syntax and examples can be obtained from `https://context7.com/websites/tanstack_query/llms.txt?tokens=10000`.
  - Do not cache server state in ad-hoc signals.

---

## 4) UI State Requirements (MANDATORY)

All data-driven UI MUST implement:
- loading
- empty
- error
- success

Make state transitions explicit and consistent.

---

## 5) Error Mapping (Frontend)

- Backend error.code values are machine-stable; frontend maps codes to user-facing zh-TW messages.
- Always surface request_id when helpful (e.g., in error UI or toast) without exposing internal details.
- Do not show raw server error strings to users.

---

## 6) Copy and i18n Rules (STRICT)

- All user-facing UI copy MUST be Traditional Chinese (zh-TW).
- Copy MUST NOT be hardcoded inline inside components.
- Centralize copy in a shared module (choose existing location; examples):
  - `src/shared/i18n/zh-TW.ts`
  - `src/shared/copy.ts`

Rules:
- Keys: English
- Values: zh-TW
- Components import keys/values; no duplicated inline copy.

Non-copy strings (keep English):
- variable/function/type names
- API field names
- error codes / analytics keys
- CSS classes / test IDs

---

## 7) Validation

- Validate critical API responses at runtime when the repo has an existing pattern:
  - Use Zod if present.
  - Otherwise, implement minimal runtime guards for critical fields.
- Do not add a new validation library unless approved.

---

## 8) Security Baseline (Frontend)

- Frontend must never store or handle secrets.
- Permission checks in frontend are UX-only; backend is authoritative.
- Avoid leaking internal details in UI errors.

---

## 9) Testing (Aligned with Global Risk-Based Policy)

- If a frontend test harness exists:
  - Add minimal tests for medium/high-risk changes.
- If not:
  - Provide manual verification steps and recommend where a test should be added later.

---

## 10) When Uncertain

STOP and ASK if unclear about:
- authentication/authorization UX flows
- money/balance/order correctness
- destructive actions or irreversible UI flows
