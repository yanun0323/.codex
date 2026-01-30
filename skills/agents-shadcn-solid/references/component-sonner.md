# Sonner

Source: https://shadcn-solid.netlify.app/docs/components/sonner

## Import

```ts
import { Toaster } from "@/components/ui/sonner"
import { toast } from "somoto"
```

## Minimal usage

```tsx
// App root (render once)
<Toaster />

// Anywhere
toast("Event has been created.")
```

## Notes

Sonner requires a single <Toaster /> mounted near the app root.
