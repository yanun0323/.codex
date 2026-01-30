# Theming

Source: https://shadcn-solid.netlify.app/docs/theming

shadcn-solid expects a token-driven theme. Prefer CSS variables + Tailwind utility bindings.

## Convention

- Use `bg-<token>` for surfaces and `text-<token>-foreground` for text.
- Example:
  - `bg-background text-foreground`
  - `bg-primary text-primary-foreground`

Avoid hard-coded colors unless you are inside a one-off marketing page.
