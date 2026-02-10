# File Field

Source: https://shadcn-solid.netlify.app/docs/components/file-field

## Import

```ts
import {
  FileField,
  FileFieldInput,
  FileFieldItem,
  FileFieldItemDeleteTrigger,
  FileFieldItemName,
  FileFieldList,
  FileFieldTrigger,
} from "@/components/ui/file-field"
```

## Minimal usage

```tsx
<FileField>
  <FileFieldTrigger>
    <FileFieldInput />
  </FileFieldTrigger>

  <FileFieldList>
    <FileFieldItem>
      <FileFieldItemName />
      <FileFieldItemDeleteTrigger />
    </FileFieldItem>
  </FileFieldList>
</FileField>
```
