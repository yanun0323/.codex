# Data Table

Source: https://shadcn-solid.netlify.app/docs/components/data-table

## Import

```ts
import type { ColumnDef } from "@tanstack/solid-table"
import { createSolidTable, flexRender, getCoreRowModel } from "@tanstack/solid-table"
import { For, Show, splitProps, type Accessor } from "solid-js"

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
```

## Minimal usage

```tsx
type Props<TData, TValue> = {
  columns: ColumnDef<TData, TValue>[]
  data: Accessor<TData[] | undefined>
}

export const DataTable = <TData, TValue>(props: Props<TData, TValue>) => {
  const [local] = splitProps(props, ["columns", "data"])

  const table = createSolidTable({
    get data() {
      return local.data() || []
    },
    columns: local.columns,
    getCoreRowModel: getCoreRowModel(),
  })

  return (
    <div class="rounded-md border">
      <Table>
        <TableHeader>
          <For each={table.getHeaderGroups()}>
            {(headerGroup) => (
              <TableRow>
                <For each={headerGroup.headers}>
                  {(header) => (
                    <TableHead>
                      {header.isPlaceholder
                        ? null
                        : flexRender(
                            header.column.columnDef.header,
                            header.getContext(),
                          )}
                    </TableHead>
                  )}
                </For>
              </TableRow>
            )}
          </For>
        </TableHeader>

        <TableBody>
          <Show
            when={table.getRowModel().rows?.length}
            fallback={
              <TableRow>
                <TableCell colSpan={local.columns.length} class="h-24 text-center">
                  No results.
                </TableCell>
              </TableRow>
            }
          >
            <For each={table.getRowModel().rows}>
              {(row) => (
                <TableRow data-state={row.getIsSelected() && "selected"}>
                  <For each={row.getVisibleCells()}>
                    {(cell) => (
                      <TableCell>
                        {flexRender(cell.column.columnDef.cell, cell.getContext())}
                      </TableCell>
                    )}
                  </For>
                </TableRow>
              )}
            </For>
          </Show>
        </TableBody>
      </Table>
    </div>
  )
}
```

## Notes

This is intentionally a *guide*, not a one-size-fits-all component. Customize columns, sorting, filtering, pagination per screen.
