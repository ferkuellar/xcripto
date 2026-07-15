/// <reference types="vite/client" />

interface ImportMetaEnv {
  /** Base URL del backend XMIP. Default: http://127.0.0.1:8000 */
  readonly VITE_API_BASE_URL?: string
  /** Browser-exposed API key placeholder (X-API-Key); never store a real secret. */
  readonly VITE_API_KEY?: string
  /** Browser-exposed RBAC role hint for internal/admin-only flows. */
  readonly VITE_ACTOR_ROLE?: string
  /** Browser-exposed actor id hint for internal/admin-only flows. */
  readonly VITE_ACTOR_ID?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
