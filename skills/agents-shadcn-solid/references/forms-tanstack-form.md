# TanStack Form + Valibot

Source: https://shadcn-solid.netlify.app/docs/forms/tanstack-form

Goal: Build accessible forms using TanStack Form's headless state + shadcn-solid input components (e.g., TextField).

## Core pattern (Field render prop)

```tsx
<form
  onSubmit={(e) => {
    e.preventDefault()
    form.handleSubmit()
  }}
>
  <form.Field name="title">
    {(field) => (
      <TextField
        validationState={
          field().state.meta.isTouched && !field().state.meta.isValid
            ? "invalid"
            : "valid"
        }
        name={field().name}
        value={field().state.value}
        onBlur={field().handleBlur}
        onChange={field().handleChange}
      >
        <TextFieldLabel>Bug Title</TextFieldLabel>
        <TextFieldInput placeholder="…" autocomplete="off" />
        <TextFieldErrorMessage errors={field().state.meta.errors} />
      </TextField>
    )}
  </form.Field>

  {/* Do not use raw <button>; use the shadcn-solid Button */}
  <Button type="submit">Submit</Button>
</form>
```

## Validation schema example (Valibot)

```ts
import * as v from "valibot"

export const formSchema = v.object({
  title: v.pipe(
    v.string(),
    v.minLength(5, "Title must be at least 5 characters."),
    v.maxLength(32, "Title must be at most 32 characters."),
  ),
})
```

## Notes

- Prefer schema validation + explicit error rendering; don't rely only on browser validation.
- For non-text fields (Select/Checkbox/RadioGroup), bind `value` + `onChange` from `field()`.
