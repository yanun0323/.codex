# Date Picker

Source: https://shadcn-solid.netlify.app/docs/components/date-picker

## Import

```ts
import { createSignal } from "solid-js"
import { format } from "date-fns"

import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
```

## Minimal usage

```tsx
const [date, setDate] = createSignal<Date>()

<Popover>
  <PopoverTrigger as={Button} variant="outline">
    {date() ? format(date(), "PPP") : <span>Pick a date</span>}
  </PopoverTrigger>
  <PopoverContent class="w-auto p-0">
    <Calendar
      mode="single"
      selected={date()}
      onSelect={(d) => setDate(d)}
      initialFocus
    />
  </PopoverContent>
</Popover>
```

## Notes

- Date Picker is a *composition* of Popover + Calendar + formatting.
- Keep the trigger accessible; don’t hide focus states.
