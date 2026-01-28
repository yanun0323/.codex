### Basic Pagination Usage (TSX)

Source: https://github.com/hngngn/shadcn-solid/blob/main/docs/src/data/docs/components/pagination.mdx

Example demonstrating how to use the Pagination component with custom item and ellipsis components.

```tsx
<Pagination
  count={10}
  itemComponent={props => <PaginationItem page={props.page}>{props.page}</PaginationItem>}
  ellipsisComponent={() => <PaginationEllipsis />}
>
  <PaginationPrevious />
  <PaginationItems />
  <PaginationNext />
</Pagination>
```