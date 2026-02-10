# Tabs

Source: https://shadcn-solid.netlify.app/docs/components/tabs

## Import

```ts
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
```

## Minimal usage

```tsx
<Tabs defaultValue="account">
  <TabsList>
    <TabsTrigger value="account">Account</TabsTrigger>
    <TabsTrigger value="password">Password</TabsTrigger>
  </TabsList>

  <TabsContent value="account">Account tab</TabsContent>
  <TabsContent value="password">Password tab</TabsContent>
</Tabs>
```

## Notes

Upstream docs sometimes show a versioned path (e.g. `.../v4/tabs`). Align this with your repo's actual file path.
