### Setup Combobox State and Filtering

Source: https://github.com/hngngn/shadcn-solid/blob/main/docs/src/data/docs/components/combobox.mdx

Define the initial list of options, create a filter instance using @kobalte/core, and set up a SolidJS signal to manage the options displayed based on the input value.

```tsx
const ALL_OPTIONS = ["Apple", "Banana", "Blueberry", "Grapes", "Pineapple"];

const filter = createFilter({ sensitivity: "base" });
const [options, setOptions] = createSignal(ALL_OPTIONS);
const onInputChange = (value: string) => {
  setOptions(ALL_OPTIONS.filter(option => filter.contains(option, value)));
};
```

--------------------------------

