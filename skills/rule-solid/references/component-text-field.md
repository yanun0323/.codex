# Text Field

Source: https://shadcn-solid.netlify.app/docs/components/text-field

## Import

```ts
import {
  TextField,
  TextFieldDescription,
  TextFieldErrorMessage,
  TextFieldInput,
  TextFieldLabel,
  TextFieldTextArea,
} from "@/components/ui/text-field"
```

## Minimal usage

```tsx
<TextField name="email" value={email()} onChange={setEmail}>
  <TextFieldLabel>Email</TextFieldLabel>
  <TextFieldInput type="email" placeholder="you@example.com" />
  <TextFieldDescription>We will never spam you.</TextFieldDescription>
  <TextFieldErrorMessage errors={errors()} />
</TextField>
```

## Notes

- For textarea, swap in `<TextFieldTextArea />`.
- Use `validationState="invalid"` to style error states consistently.
