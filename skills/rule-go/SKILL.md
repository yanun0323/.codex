---
name: rule-go
description: Rules for Go backend work - project identity, layering, error handling, concurrency, initialization, API contracts, testing, and infra triggers.
---

# Go Backend Rules

## Project Identity

Assume a monolithic Go backend with sole entry point `cmd/server/main.go`. Do not add binaries, root `main.go`, or business logic in `cmd/server`. If the repo clearly disagrees, stop and ask.

## Dependencies

Follow existing choices first. If absent, prefer: config `viper`, log `zerolog/log`, HTTP `echo/v4`, websocket `gorilla/websocket`, ORM `gorm`, JSON `sonic`. Do not replace equivalents or add non-recommended dependencies unless asked. Keep `viper` in `config/` and bootstrap; inject typed config into app layers.

## Ownership

- `cmd/server`: wiring/bootstrap only
- `config`: schemas/defaults/loaders
- `internal/delivery`: transport, validation, mapping
- `internal/usecase`: business logic
- `internal/repository`: persistence
- `internal/model`: domain entities
- `internal/model/enum`: domain entities enum
- `internal/adapter`: ports/interfaces
- `infrastructure`: Docker/compose/k8s/deploy
- `pkg`: stateless shared utilities only

Do not reorganize folders unless requested.

## Imports

`model -> enum`; `model -> pkg`; `adapter -> model,enum,pkg`; `delivery/usecase/repository -> adapter,model,enum,pkg`; `config -> pkg`; `pkg` must not import `internal/config/cmd`. Cross-layer violations are hard errors; ask if unclear.

## Runtime Rules

- Handlers parse/validate, call ports, and map responses; no business logic or storage access.
- Respect request context; external calls need cancellable timeouts.
- Never panic in app code. Return/handle errors explicitly.
- Wrap with `%w` only when callers need the cause.
- Do not log and return the same error at the same layer.
- Never expose internals to clients; use stable machine codes and safe messages.
- No fire-and-forget goroutines; every goroutine needs context or shutdown channel.
- `init()` is forbidden; initialization must trace from `cmd/server/main.go`.

## API/Style/Tests

Preserve existing API envelope/status conventions. Keep changes minimal; no unrelated refactors or exported API renames. Follow Go naming. New/changed endpoints need existing-pattern tests for success, validation failure, and one edge case unless forbidden; otherwise give manual verification.

## Infra and Stop Conditions

If adding ports, env vars, external dependencies, runtime/build changes, follow infra rules. Stop and ask for unclear auth/permission, money/order invariants, irreversible migration, concurrency lifecycle, or layer ownership disputes.
