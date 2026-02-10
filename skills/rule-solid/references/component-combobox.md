# Combobox

Source: https://shadcn-solid.netlify.app/docs/components/combobox

## Import

```ts
import {
  Combobox,
  ComboboxContent,
  ComboboxInput,
  ComboboxItem,
  ComboboxTrigger,
} from "@/components/ui/combobox"
```

## Minimal usage

```tsx
<Combobox>
  <ComboboxTrigger>
    <ComboboxInput placeholder="Search…" />
  </ComboboxTrigger>
  <ComboboxContent>
    <ComboboxItem item="apple">Apple</ComboboxItem>
  </ComboboxContent>
</Combobox>
```

## Notes

Upstream docs show `ComboboxInput` usage; ensure it is imported/exported correctly in your local module.
