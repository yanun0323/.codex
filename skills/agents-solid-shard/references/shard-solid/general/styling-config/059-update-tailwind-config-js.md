### Update Tailwind Config (JS)

Source: https://github.com/hngngn/shadcn-solid/blob/main/docs/src/data/docs/components/otp-field.mdx

Update your tailwind.config.cjs file to include necessary keyframes and animations for component functionality. This specific example shows keyframes for accordion animations, which might be a copy-paste error in the source text, but is presented as part of the OTP field installation.

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      keyframes: {
        "accordion-down": {
          from: { height: 0 },
          to: { height: "var(--kb-accordion-content-height)" }
        },
        "accordion-up": {
          from: { height: "var(--kb-accordion-content-height)" },
          to: { height: 0 }
        }
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out"
      }
    }
  }
};
```

--------------------------------

