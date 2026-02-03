# Sidebar

Source: https://shadcn-solid.netlify.app/docs/components/sidebar

## Import

```ts
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar"
```

## Minimal usage

```tsx
<SidebarProvider>
  <Sidebar>
    <SidebarHeader>Header</SidebarHeader>
    <SidebarContent>Nav items</SidebarContent>
    <SidebarFooter>Footer</SidebarFooter>
  </Sidebar>

  {/* Your main page content */}
  <main class="flex-1">
    <SidebarTrigger />
    {/* ... */}
  </main>
</SidebarProvider>
```

## Notes

Sidebar is a layout system and tends to be app-specific. If this doesn’t compile, open the upstream page and copy the canonical sidebar implementation into your repo, then adapt.
