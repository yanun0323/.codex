# Breadcrumbs

Source: https://shadcn-solid.netlify.app/docs/components/breadcrumbs

## Import

```ts
import {
  BreadcrumbList,
  Breadcrumbs,
  BreadcrumbsItem,
  BreadcrumbsLink,
  BreadcrumbsSeparator,
} from "@/components/ui/breadcrumbs"
```

## Minimal usage

```tsx
<Breadcrumbs>
  <BreadcrumbList>
    <BreadcrumbsItem>
      <BreadcrumbsLink href="/">Home</BreadcrumbsLink>
    </BreadcrumbsItem>
    <BreadcrumbsSeparator />
    <BreadcrumbsItem>
      <BreadcrumbsLink href="/settings">Settings</BreadcrumbsLink>
    </BreadcrumbsItem>
  </BreadcrumbList>
</Breadcrumbs>
```

## Notes

Upstream docs sometimes use an `@components/*` alias. Normalize imports to your repo’s alias.
