---
name: agents-go
description: Rules for Go backend work - project identity, layering, error handling, concurrency, initialization, API contracts, testing, and infra triggers.
---

# Go Backend Rules

## When to Use
- Load this skill when working on the Go backend or reviewing Go server changes.

If any rule conflicts with explicit user instructions, follow the user instructions.
If any rule conflicts with the agents-global skill, follow the higher-priority rule defined there.

---

## 1) Project Identity (HARD)

- This repository contains a monolithic Go backend service.
- Single main binary: `cmd/server`
- The ONLY application entry point is:
  - `cmd/server/main.go`

HARD rules:
- Do NOT create additional binaries unless explicitly requested.
- Do NOT put business logic in `cmd/server/main.go`.
- Do NOT create or use a root-level `main.go` as an entry point.
  - If `main.go` exists at repo root, it must contain no logic and must not be used.

If this project identity does not match the actual repository, STOP and ASK.

---

## 2) Framework and Dependencies

- Prefer standard library over third-party packages.
- Do NOT introduce new dependencies unless explicitly instructed.

### Recommended packages (follow repo conventions first)

If the repo already uses an equivalent external or in-house package for the same purpose, use the repo's existing choice instead of switching.

- environment/config: github.com/spf13/viper
- log: github.com/rs/zerolog/log
- http: github.com/labstack/echo/v4
- websocket: github.com/gorilla/websocket
- sql orm: gorm.io/gorm

---

## 3) Folder Ownership (HARD)

Agents MUST respect the following folder responsibilities:

| Folder              | Responsibility                                            |
| ------------------- | --------------------------------------------------------- |
| cmd/server          | Application wiring only (bootstrap, dependency injection) |
| internal/delivery   | Transport layer (HTTP handlers, request/response mapping) |
| internal/usecase    | Business logic (application rules)                        |
| internal/repository | Persistence / storage logic                               |
| internal/model      | Domain entities and enums                                 |
| internal/adapter    | Interface abstractions (ports/adapters)                   |
| infrastructure      | Runtime infra (Docker, compose, k8s, deployment)          |
| pkg                 | Shared, stateless utilities ONLY                          |

If the existing repo differs in naming but clearly follows the same layering,
follow the repo's established structure. Do NOT reorganize folders unless instructed.

---

## 4) Boundary and Import Rules (HARD)

HARD rules:
- `internal/delivery` MUST NOT contain business logic.
- `internal/usecase` MUST NOT depend on `internal/delivery`.
- `internal/repository` MUST NOT depend on `internal/delivery`.
- `pkg` MUST NOT depend on `internal`.
- Cross-layer imports that violate the above are HARD ERRORS.

If you are unsure whether an import violates layering, STOP and ASK.

---

## 5) Delivery Rules

### 5.1 Handler Responsibilities
Handlers in `internal/delivery` MUST:
- Parse and validate inputs (path/query/body)
- Map inputs to usecase calls
- Map usecase outputs/errors to HTTP responses

Handlers MUST NOT:
- Contain business rules
- Directly access database/storage
- Embed long-running logic without delegation to usecase

### 5.2 Context and Timeouts
- All request handling MUST respect the request context.
- External calls (DB/HTTP/etc.) must have timeouts and be cancellable.

### 5.3 Middleware (Follow Existing Repo)
If the repo already has middleware conventions, follow them.
Recommended (do not introduce new conventions if repo differs):
- Request ID: propagate `X-Request-Id` or generate; return it in response headers.
- Logging: one structured line per request (request_id, route, status, duration_ms).
- Recovery: use recovery middleware if present (no panics in app code).

---

## 6) Error Handling (HARD)

HARD rules:
- NEVER panic in application code.
- Errors MUST be returned or handled explicitly.
- Use `%w` wrapping ONLY when callers need access to the underlying cause.
- Do NOT log and return the same error at the same layer.
  - Either log at a boundary OR return upward, not both.

Client-facing rules:
- Never expose internal error strings, stack traces, SQL, hostnames, or infrastructure details.
- Use stable machine error codes (consumed by frontend) and user-safe messages.

---

## 7) Concurrency and Lifecycle (HARD)

HARD rules:
- NEVER start goroutines without a shutdown mechanism.
- Every goroutine MUST be:
  - cancellable via context OR
  - stoppable via a channel and wired into shutdown

Forbidden:
- Fire-and-forget goroutines

If concurrency lifecycle is unclear, STOP and ASK.

---

## 8) Initialization Rules (HARD)

- `init()` functions are FORBIDDEN.
- All initialization MUST be explicit and traceable from `cmd/server/main.go`.

---

## 9) API Contract and Status Codes (Follow Repo; Recommend Consistency)

If the repo already has an established API envelope and error format, DO NOT change it.
Follow the existing patterns.

If the repo has no standard, prefer a consistent format such as:

Success:
{
  "data": <payload>,
  "meta": { "request_id": "..." }
}

Error:
{
  "error": {
    "code": "<machine_code>",
    "message": "<user_safe_message>",
    "details": <optional_object>
  },
  "meta": { "request_id": "..." }
}

Recommended status codes:
- 200/201: success
- 400: validation / bad request
- 401/403: auth / permission
- 404: not found
- 409: conflict (state mismatch)
- 429: rate limit
- 500: unexpected

---

## 10) Code Modification Policy (HARD)

- Fix issues by modifying the actual problematic code.
- Keep changes minimal and localized.
- Do NOT refactor unrelated code.
- Do NOT rename exported APIs unless explicitly requested.

---

## 11) Naming and Style

- Follow standard Go naming conventions.
- Package names: lowercase, no underscores.
- Exported errors use `ErrXxx`.

---

## 12) Testing (Aligned with Global Risk-Based Policy)

Default:
- Medium risk by default for new endpoints/feature logic.

For new/changed endpoints (unless user forbids tests):
- Add minimal tests following existing patterns:
  - success path
  - validation failure
  - one meaningful edge case

If tests are forbidden or infeasible:
- Provide a precise manual verification checklist (HTTP requests, expected status/body, edge cases).

---

## 13) Infra Triggers

If your change introduces:
- new ports
- new env vars
- new external dependencies (DB/cache/queue)
- runtime/build changes

Then you MUST follow the agents-infra skill and update infra files accordingly.

---

## 14) When to STOP and ASK (HARD)

STOP and ASK if unclear about:
- Auth boundary / permission model
- Money/balance/order invariants
- Data migration / irreversible changes
- Concurrency lifecycle / shutdown wiring
- Any cross-layer ownership dispute
