# Dark Mode

Source: https://shadcn-solid.netlify.app/docs/dark-mode

shadcn-solid docs show a Kobalte-based ColorModeProvider approach.

## Minimal integration (Solid Start style)

```tsx
import { Suspense } from "solid-js"
import { isServer } from "solid-js/web"
import {
  ColorModeProvider,
  ColorModeScript,
  cookieStorageManagerSSR,
} from "@kobalte/core"
import { Router } from "@solidjs/router"
import { FileRoutes } from "@solidjs/start"
import { getCookie } from "vinxi/http"

const getServerCookies = () => {
  "use server"
  const colorMode = getCookie("kb-color-mode")
  return colorMode ? `kb-color-mode=${colorMode}` : ""
}

export default function App() {
  const storageManager = cookieStorageManagerSSR(
    isServer ? getServerCookies() : document.cookie,
  )

  return (
    <>
      <ColorModeScript />
      <ColorModeProvider storageManager={storageManager}>
        <Router
          root={(props) => (
            <Suspense>
              {props.children}
            </Suspense>
          )}
        >
          <FileRoutes />
        </Router>
      </ColorModeProvider>
    </>
  )
}
```

Notes:
- Keep cookie key consistent with Kobalte defaults (`kb-color-mode`).
- If your app isn't Solid Start, adapt the root entry accordingly.
