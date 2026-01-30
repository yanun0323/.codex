# Drawer

Source: https://shadcn-solid.netlify.app/docs/components/drawer

## Import

```ts
import {
  Drawer,
  DrawerClose,
  DrawerContent,
  DrawerDescription,
  DrawerFooter,
  DrawerHeader,
  DrawerOverlay,
  DrawerTitle,
  DrawerTrigger,
} from "@/components/ui/drawer"
```

## Minimal usage

```tsx
<Drawer>
  <DrawerTrigger>Open</DrawerTrigger>
  <DrawerOverlay>
    <DrawerContent>
      <DrawerHeader>
        <DrawerTitle>Title</DrawerTitle>
        <DrawerDescription>Description</DrawerDescription>
      </DrawerHeader>
      <DrawerFooter>
        <DrawerClose>Close</DrawerClose>
      </DrawerFooter>
    </DrawerContent>
  </DrawerOverlay>
</Drawer>
```
