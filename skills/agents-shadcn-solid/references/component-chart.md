# Chart

Source: https://shadcn-solid.netlify.app/docs/components/chart

## Import

```ts
import { VisArea, VisTooltip } from "@unovis/solid"
import {
  ChartContainer,
  ChartCrosshair,
  ChartTooltipContent,
} from "@/components/ui/charts"
```

## Minimal usage

```tsx
<ChartContainer data={data} type="xy" config={chartConfig}>
  <VisArea x={(d) => d.month} y={(d) => d.desktop} />
  <ChartCrosshair
    template={(props) => (
      <ChartTooltipContent labelKey="month" indicator="line" {...props} />
    )}
  />
  <VisTooltip />
</ChartContainer>
```

## Notes

Charts are built on Unovis. Treat this as a higher-level wrapper for consistent theming + tooltip rendering.
