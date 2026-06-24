---
name: rule-make
description: Create or update standard build/test/run entrypoints via Makefile or equivalent package scripts, with env and Docker wrappers when requested.
---

# Makefile Rules

- Standardize active repos around clear `build`, `test`, and `run` entrypoints.
- Prefer `make build`, `make test`, and `make run` when a repo has or needs a Makefile.
- For `package.json` repos, equivalent `build`, `test`, and `run` package scripts are acceptable; Makefile targets may delegate to them when Makefile is the Codex entrypoint.
- For `Package.swift` repos, prefer Makefile targets wrapping `swift build`, `swift test`, and `swift run` unless an equivalent standard entrypoint already exists.
- Keep Makefiles minimal and wrap existing repo commands.
- Do not add dependencies, change toolchains, or restructure architecture just to create entrypoints.
- Every target needs a `## ` help comment.
- Use wildcard `.PHONY`: `.PHONY: $(wildcard *)`.
- `Makefile.env` is git-ignored build/deploy env; `Makefile.local.env` is committed local template only when needed and may override `Makefile.env`.
- Do not hardcode secrets.
- Typical targets: `run`, `dev`, `build`, `test`, `lint`, `fmt`, `clean`; add only supported workflows.
- For Docker requests, wrap existing files with `docker-build`, `docker-run`, `compose-up`, `compose-down`, `compose-logs`; prefer `docker compose` unless repo uses `docker-compose`.
- If ports/env/services/build change, follow infra rules.

## Base Template

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

ARGS := $(word 2,$(MAKECMDGOALS))
%:
	@:
```

Add `-include Makefile.local.env` after `Makefile.env` only when local env is needed. Targets that require it should source it explicitly with `set -a; . ./Makefile.local.env; set +a; ...`.
