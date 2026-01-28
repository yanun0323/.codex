### Show a Basic Toast (SolidJS/TSX)

Source: https://github.com/hngngn/shadcn-solid/blob/main/docs/src/data/docs/components/toast.mdx

Demonstrate how to programmatically display a basic toast message using the `toaster.show` function. This example shows a simple toast with a title and progress bar.

```tsx
toaster.show(props => (
  <Toast toastId={props.toastId}>
    <ToastContent>
      <ToastTitle>Toast</ToastTitle>
    </ToastContent>
    <ToastProgress />
  </Toast>
))
```

--------------------------------

