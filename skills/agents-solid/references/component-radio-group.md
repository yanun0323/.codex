# Radio Group

Source: https://shadcn-solid.netlify.app/docs/components/radio-group

## Import

```ts
import {
  RadioGroup,
  RadioGroupItem,
  RadioGroupItemControl,
  RadioGroupItemIndicator,
  RadioGroupItemInput,
  RadioGroupItemLabel,
  RadioGroupItems,
  RadioGroupLabel,
} from "@/components/ui/radio-group"
```

## Minimal usage

```tsx
<RadioGroup>
  <RadioGroupLabel>Theme</RadioGroupLabel>
  <RadioGroupItems>
    <RadioGroupItem value="light">
      <RadioGroupItemInput />
      <RadioGroupItemControl>
        <RadioGroupItemIndicator />
      </RadioGroupItemControl>
      <RadioGroupItemLabel>Light</RadioGroupItemLabel>
    </RadioGroupItem>

    <RadioGroupItem value="dark">
      <RadioGroupItemInput />
      <RadioGroupItemControl>
        <RadioGroupItemIndicator />
      </RadioGroupItemControl>
      <RadioGroupItemLabel>Dark</RadioGroupItemLabel>
    </RadioGroupItem>
  </RadioGroupItems>
</RadioGroup>
```

## Notes

Upstream docs sometimes omit `RadioGroupItem` from the import list. Ensure your local module exports it.
