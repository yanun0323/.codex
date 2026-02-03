# Tooltip

Source: https://shadcn-solid.netlify.app/docs/components/tooltip

## Import

```ts
import {
  Tooltip,
  TooltipContent,
  TooltipPortal,
  TooltipTrigger,
} from "@/components/ui/tooltip"
```

## Minimal usage

```tsx
<Tooltip>
  <TooltipTrigger>Hover</TooltipTrigger>
  <TooltipPortal>
    <TooltipContent>Tooltip content</TooltipContent>
  </TooltipPortal>
</Tooltip>
```
