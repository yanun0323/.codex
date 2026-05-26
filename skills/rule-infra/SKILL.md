---
name: rule-infra
description: Infra, container, and configuration rules for changes that affect runtime interfaces, ports, env vars, or dependencies.
---

# Infra Rules

Apply only when adding/changing services, exposed ports, env vars, runtime dependencies, build steps, or runtime behavior. Otherwise leave Docker/compose/k8s untouched.

## Security

- Never hardcode secrets in code, images, or compose.
- Runtime config must be injectable through env vars or Kubernetes ConfigMap/Secret.
- Defaults must be non-sensitive, local-dev safe, and documented.

## Docker

When required, follow existing style; prefer multi-stage builds, pinned non-`latest` bases, non-root final image, no environment-specific baked values, and minimal runtime image.

## Compose/Kubernetes

Use explicit service names, env placeholders, no secrets, explicit networks for multi-service stacks, and existing healthcheck patterns. Avoid unrelated service edits. Assume Kubernetes config via env, mounted files only when explicit, readiness/liveness consistent with repo.

## Output

Report what changed and why, env var names only, migration notes for new dependencies, and verification commands for build/run/compose smoke tests.
