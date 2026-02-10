# Navigation Menu

Source: https://shadcn-solid.netlify.app/docs/components/navigation-menu

## Import

```ts
import {
  NavigationItemDescription,
  NavigationItemLabel,
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuItem,
  NavigationMenuList,
  NavigationMenuPortal,
  NavigationMenuTrigger,
} from "@/components/ui/navigation-menu"
```

## Minimal usage

```tsx
<NavigationMenu>
  <NavigationMenuList>
    <NavigationMenuItem>
      <NavigationMenuTrigger>Getting started</NavigationMenuTrigger>
      <NavigationMenuPortal>
        <NavigationMenuContent>
          <a href="/docs">
            <NavigationItemLabel>Docs</NavigationItemLabel>
            <NavigationItemDescription>
              Read the documentation.
            </NavigationItemDescription>
          </a>
        </NavigationMenuContent>
      </NavigationMenuPortal>
    </NavigationMenuItem>
  </NavigationMenuList>
</NavigationMenu>
```

## Notes

This is a composable nav primitive. Keep the trigger + portal + content structure; don’t inline menus with absolute-position divs.
