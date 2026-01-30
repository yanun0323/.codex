# Installation

Source: https://shadcn-solid.netlify.app/docs/installation

This is not a step-by-step installer script; it's a checklist.

## What you should verify in the repo

- TailwindCSS (or UnoCSS) is installed and configured.
- The shared utilities exist (e.g. `src/lib/cva.ts`, `src/lib/call-handler.ts`, `src/lib/combine-style.ts`, `src/hooks/use-mobile.ts`).
- The shadcn-solid UI components are present under the repo's UI layer (commonly `src/components/ui/*`).

If any of those are missing, add them first; otherwise component imports in references won't compile.
