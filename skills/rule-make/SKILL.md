---
name: rule-make
description: Create or update Makefile targets to run/build/test apps, inject env via Makefile.env/Makefile.local.env, and add docker/compose shortcuts when requested.
metadata:
  short-description: Makefile workflow and env injection
---

# Makefile Rules

- Keep Makefiles minimal and wrap existing repo commands.
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
