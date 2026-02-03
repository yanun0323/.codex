# Popover

Source: https://shadcn-solid.netlify.app/docs/components/popover

## Import

```ts
import {
  Popover,
  PopoverContent,
  PopoverPortal,
  PopoverTrigger,
} from "@/components/ui/popover"
```

## Minimal usage

```tsx
<Popover>
  <PopoverTrigger>Open</PopoverTrigger>
  <PopoverPortal>
    <PopoverContent>Content</PopoverContent>
  </PopoverPortal>
</Popover>
```
