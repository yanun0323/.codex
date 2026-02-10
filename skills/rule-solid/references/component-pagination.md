# Pagination

Source: https://shadcn-solid.netlify.app/docs/components/pagination

## Import

```ts
import {
  Pagination,
  PaginationEllipsis,
  PaginationItem,
  PaginationItems,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination"
```

## Minimal usage

```tsx
<Pagination
  count={10}
  itemComponent={(props) => (
    <PaginationItem page={props.page}>{props.page}</PaginationItem>
  )}
  ellipsisComponent={() => <PaginationEllipsis />}
>
  <PaginationPrevious />
  <PaginationItems />
  <PaginationNext />
</Pagination>
```
