# Menubar

Source: https://shadcn-solid.netlify.app/docs/components/menubar

## Import

```ts
import {
  Menubar,
  MenubarContent,
  MenubarItem,
  MenubarMenu,
  MenubarPortal,
  MenubarTrigger,
} from "@/components/ui/menubar"
```

## Minimal usage

```tsx
<Menubar>
  <MenubarMenu>
    <MenubarTrigger>File</MenubarTrigger>
    <MenubarPortal>
      <MenubarContent>
        <MenubarItem>New</MenubarItem>
        <MenubarItem>Open…</MenubarItem>
      </MenubarContent>
    </MenubarPortal>
  </MenubarMenu>
</Menubar>
```

## Notes

Menubar subcomponent names may vary depending on your local implementation. If this doesn’t compile, open `src/components/ui/menubar.tsx` and align names.
