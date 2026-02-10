---
name: rule-infra
description: Infra, container, and configuration rules for changes that affect runtime interfaces, ports, env vars, or dependencies.
---

# Infra, Containerization, and Configuration Rules

## When to Use
- Load this skill when a change impacts runtime interface or deployment (ports, env vars, services, build/runtime behavior).

If any rule conflicts with explicit user instructions, follow the user instructions.
If any rule conflicts with the rule-global skill, follow the higher-priority rule defined there.

---

## 1) Trigger Conditions (When This Skill Applies)

Infrastructure updates are REQUIRED only when any of the following changes:
- A new service is introduced (db/cache/queue/worker/etc.)
- Ports change or new ports are exposed
- New environment variables are added or existing ones are renamed/removed
- Runtime dependencies change (e.g., add Redis/Postgres/S3)
- Build/runtime behavior changes (new build steps, new static assets pipeline, etc.)

Otherwise:
- Dockerfile and docker-compose files MUST remain unchanged.

---

## 2) Secrets and Configuration Injection (HARD)

- Never hardcode secrets in code, images, or compose files.
- All runtime config must be injectable via:
  - Environment variables
  - Kubernetes ConfigMap/Secret

Defaults are allowed ONLY if:
- non-sensitive
- safe for local dev
- clearly documented

---

## 3) Dockerfile Rules (Production-Oriented)

When a Dockerfile change is required:
- Prefer multi-stage builds where applicable.
- Pin base images to a specific version (no `latest`).
- Final image should run as non-root (unless explicitly required).
- Do not bake environment-specific values into the image.
- Keep image minimal (remove build tools from runtime stage).

If the repo already has a Dockerfile style, follow it and improve only as needed.

---

## 4) docker-compose Rules

When compose changes are required:
- Use explicit service names.
- Use env vars and `.env` placeholders where appropriate.
- Do not embed secrets.
- Declare networks explicitly when multiple services are involved.
- Prefer healthchecks if the repo already uses them.

Avoid changing unrelated services.

---

## 5) Kubernetes Compatibility Contract

Assume deployment via Kubernetes:
- Configuration via env (ConfigMap/Secret)
- No reliance on local filesystem paths unless explicitly mounted
- Use readiness/liveness patterns consistent with the repo

---

## 6) Infra Change Output Requirements

When infra triggers apply, include in your response:
- What changed and why (ports/env/deps)
- Updated env var list (names only, no values)
- Migration notes (if a new dependency is introduced)
- Verification steps:
  - build command(s)
  - container run command(s)
  - compose up smoke test steps
