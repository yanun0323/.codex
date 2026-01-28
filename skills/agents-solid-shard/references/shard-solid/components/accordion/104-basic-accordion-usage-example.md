### Basic Accordion Usage Example

Source: https://github.com/hngngn/shadcn-solid/blob/main/docs/src/data/docs/components/accordion.mdx

Demonstrates a basic implementation of the Accordion component with a single collapsible item, showing how to structure the components and add content.

```tsx
<Accordion type="single" collapsible>
  <AccordionItem value="item-1">
    <AccordionTrigger>Is it accessible?</AccordionTrigger>
    <AccordionContent>Yes. It adheres to the WAI-ARIA design pattern.</AccordionContent>
  </AccordionItem>
</Accordion>
```

--------------------------------

