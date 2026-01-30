# Segmented Control

Source: https://shadcn-solid.netlify.app/docs/components/segmented-control

## Import

```ts
import { createSignal } from "solid-js"
import { SegmentedControl, SegmentedControlItem } from "@/components/ui/segmented-control"
```

## Minimal usage

```tsx
const [value, setValue] = createSignal("active")

<SegmentedControl value={value()} onChange={setValue}>
  <SegmentedControlItem value="inactive">Inactive</SegmentedControlItem>
  <SegmentedControlItem value="active">Active</SegmentedControlItem>
</SegmentedControl>
```
