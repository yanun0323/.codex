### Configure Path Alias in tsconfig.json - JSON

Source: https://github.com/hngngn/shadcn-solid/blob/main/docs/src/data/docs/installation/manual.mdx

Configure the TypeScript compiler options to set up a path alias, typically '@', mapping it to the source directory. This simplifies import paths for components and modules.

```json
{
  "compilerOptions": {
    "baseUrl": "./",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

--------------------------------

