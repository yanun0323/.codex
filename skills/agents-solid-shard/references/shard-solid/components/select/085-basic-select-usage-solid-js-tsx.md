### Basic Select Usage (Solid.js) - TSX

Source: https://github.com/hngngn/shadcn-solid/blob/main/docs/src/data/docs/components/select.mdx

Example demonstrating the basic structure and usage of the Select component with a list of string options.

```tsx
<Select
  options={["Apple", "Banana", "Blueberry", "Grapes", "Pineapple"]}
  itemComponent={props => <SelectItem item={props.item}>{props.item.rawValue}</SelectItem>}
>
  <SelectTrigger>
    <SelectValue<string>>{state => state.selectedOption()}</SelectValue>
  </SelectTrigger>
  <SelectContent />
</Select>
```

--------------------------------

