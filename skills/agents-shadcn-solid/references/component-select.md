# Select

Source: https://shadcn-solid.netlify.app/docs/components/select

## Import

```ts
import {
  Select,
  SelectContent,
  SelectItem,
  SelectPortal,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
```

## Minimal usage

```tsx
<Select>
  <SelectTrigger>
    <SelectValue placeholder="Select a fruit" />
  </SelectTrigger>

  <SelectPortal>
    <SelectContent>
      <SelectItem item="apple">Apple</SelectItem>
      <SelectItem item="banana">Banana</SelectItem>
    </SelectContent>
  </SelectPortal>
</Select>
```
