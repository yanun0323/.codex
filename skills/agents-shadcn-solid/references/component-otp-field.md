# OTP Field

Source: https://shadcn-solid.netlify.app/docs/components/otp-field

## Import

```ts
import {
  OTPField,
  OTPFieldGroup,
  OTPFieldInput,
  OTPFieldSeparator,
  OTPFieldSlot,
} from "@/components/ui/otp-field"
```

## Minimal usage

```tsx
<OTPField>
  <OTPFieldInput />
  <OTPFieldGroup>
    <OTPFieldSlot index={0} />
    <OTPFieldSlot index={1} />
    <OTPFieldSlot index={2} />
  </OTPFieldGroup>
  <OTPFieldSeparator />
  <OTPFieldGroup>
    <OTPFieldSlot index={3} />
    <OTPFieldSlot index={4} />
    <OTPFieldSlot index={5} />
  </OTPFieldGroup>
</OTPField>
```
