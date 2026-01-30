# Number Field

Source: https://shadcn-solid.netlify.app/docs/components/number-field

## Import

```ts
import {
  NumberField,
  NumberFieldDecrementTrigger,
  NumberFieldGroup,
  NumberFieldIncrementTrigger,
  NumberFieldInput,
  NumberFieldLabel,
} from "@/components/ui/number-field"
```

## Minimal usage

```tsx
<NumberField>
  <NumberFieldLabel>Quantity</NumberFieldLabel>
  <NumberFieldGroup>
    <NumberFieldInput />
    <NumberFieldDecrementTrigger />
    <NumberFieldIncrementTrigger />
  </NumberFieldGroup>
</NumberField>
```
