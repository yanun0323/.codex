### Basic Dialog Usage Example

Source: https://github.com/hngngn/shadcn-solid/blob/main/docs/src/data/docs/components/dialog.mdx

Demonstrates a simple implementation of the Dialog component with a trigger, header, title, and description.

```tsx
<Dialog>
  <DialogTrigger>Open</DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Are you sure absolutely sure?</DialogTitle>
      <DialogDescription>
        This action cannot be undone. This will permanently delete your account and remove your data
        from our servers.
      </DialogDescription>
    </DialogHeader>
  </DialogContent>
</Dialog>
```

--------------------------------

