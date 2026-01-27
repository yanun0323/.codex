---
name: agents-make
description: Create or update Makefile targets to run/build/test apps, inject env via Makefile.env/Makefile.local.env, and add docker/compose shortcuts when requested.
metadata:
  short-description: Makefile workflow and env injection
---

# Makefile Workflow

## When to Use
- Use this skill when the user asks to add or update a Makefile, make targets, or make-based shortcuts for running, building, or testing a project.

## Core Rules
- Keep the Makefile minimal and aligned with existing project commands (scripts, package.json, Go tooling, etc.).
- Prefer wrapping existing scripts or commands instead of inventing new workflows.
- Every target must include a `## ` comment so it appears in `make help` output.
- Avoid long `.PHONY` lists; use the wildcard pattern below.

## Environment Injection
- Use `Makefile.env` for build/deploy-related environment variables.
- Use `Makefile.local.env` as a repo-committed template for local development environment variables.
- `Makefile.env` should be git-ignored; `Makefile.local.env` can be committed.
- Only include `Makefile.local.env` when local env vars are needed. If included, it should override `Makefile.env`.
- Do not hardcode secrets.

## Template (Required)
Use this template as the base. Add `-include Makefile.local.env` only when needed.

```make
-include Makefile.env
export

.PHONY: $(wildcard *)

## help: show help
help:
	@echo ""
	@echo "Usage:"
	@echo ""
	@sed -n 's/^## //p' Makefile | column -t -s ':' | sed -e 's/^/\t/'
	@echo ""

## run: go run particular folder
run:
	@if [ -z "$(ARGS)" ]; then \
	    echo "go run main.go"; go run main.go; \
	fi
	@echo "go run $(ARGS)" \
	go run $(ARGS)

## test: go test particular folder
test:
	@if [ -z "$(ARGS)" ]; then \
	    echo "go test ./..."; go test --count=1 ./...; \
	fi
	@echo "go test $(ARGS)" \
	go test --count=1 $(ARGS)
```

If local env is required, insert this line after `-include Makefile.env`:

```make
-include Makefile.local.env
```

When a target requires values from `Makefile.local.env`, load it explicitly:

```make
## dev-run: example target that loads Makefile.local.env
dev-run:
\t@set -a; . ./Makefile.local.env; set +a; \\
\t\trun something...
```

## Target Patterns
- `run`, `dev`, `build`, `test`, `lint`, `fmt`, `clean` are typical. Only add what the repo already supports.
- Use shell-safe commands and inherit env via `export` from the template.

## Docker / Compose Shortcuts
If the request includes Docker or docker-compose:
- Add make targets that wrap the existing Dockerfile and compose file names.
- Prefer `docker compose` (v2) unless the repo clearly uses `docker-compose`.
- Typical targets: `docker-build`, `docker-run`, `compose-up`, `compose-down`, `compose-logs`.
- If infra changes are needed (ports/env/services/build), load and follow `agents-infra`.
