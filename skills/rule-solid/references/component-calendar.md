# Calendar

Source: https://shadcn-solid.netlify.app/docs/components/calendar

## Import

```ts
import { createSignal } from "solid-js"
import { Calendar } from "@/components/ui/calendar"
```

## Minimal usage

```tsx
const [value, setValue] = createSignal<Date>()

<Calendar value={value()} onChange={setValue} />
```

## Notes

Calendar often becomes part of Date Picker (Popover + Calendar + date formatting).
