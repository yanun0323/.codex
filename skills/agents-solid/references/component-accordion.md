# Accordion

Source: https://shadcn-solid.netlify.app/docs/components/accordion

## Import

```ts
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion"
```

## Minimal usage

```tsx
<Accordion>
  <AccordionItem value="item-1">
    <AccordionTrigger>Section title</AccordionTrigger>
    <AccordionContent>Section content</AccordionContent>
  </AccordionItem>
</Accordion>
```

## Notes

- Use `value` on items for stable identity.
- Keep triggers as actual interactive elements; don’t replace with plain divs.
