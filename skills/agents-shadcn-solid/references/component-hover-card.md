# Hover Card

Source: https://shadcn-solid.netlify.app/docs/components/hover-card

## Import

```ts
import {
  HoverCard,
  HoverCardContent,
  HoverCardPortal,
  HoverCardTrigger,
} from "@/components/ui/hover-card"
```

## Minimal usage

```tsx
<HoverCard>
  <HoverCardTrigger>Hover me</HoverCardTrigger>
  <HoverCardPortal>
    <HoverCardContent>Preview</HoverCardContent>
  </HoverCardPortal>
</HoverCard>
```
