# Context Menu

Source: https://shadcn-solid.netlify.app/docs/components/context-menu

## Import

```ts
import {
  ContextMenu,
  ContextMenuContent,
  ContextMenuItem,
  ContextMenuTrigger,
} from "@/components/ui/context-menu"
```

## Minimal usage

```tsx
<ContextMenu>
  <ContextMenuTrigger>Right click me</ContextMenuTrigger>
  <ContextMenuContent>
    <ContextMenuItem>Action</ContextMenuItem>
  </ContextMenuContent>
</ContextMenu>
```
