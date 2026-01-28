### Basic Menubar Usage Example - TSX

Source: https://github.com/hngngn/shadcn-solid/blob/main/docs/src/data/docs/components/menubar.mdx

Demonstrates a basic implementation of the Menubar component in TSX, showing how to structure a menu with items, separators, and shortcuts.

```tsx
<Menubar>
  <MenubarMenu>
    <MenubarTrigger>File</MenubarTrigger>
    <MenubarContent>
      <MenubarItem>
        New Tab <MenubarShortcut>⌘T</MenubarShortcut>
      </MenubarItem>
      <MenubarItem>New Window</MenubarItem>
      <MenubarSeparator />
      <MenubarItem>Share</MenubarItem>
      <MenubarSeparator />
      <MenubarItem>Print</MenubarItem>
    </MenubarContent>
  </MenubarMenu>
</Menubar>
```

--------------------------------

