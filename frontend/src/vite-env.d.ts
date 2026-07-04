/// <reference types="vite/client" />

interface ImportMetaEnv {
  /** Base URL del backend XMIP. Default: http://127.0.0.1:8000 */
  readonly VITE_API_BASE_URL?: string
  /** API key opcional (X-API-Key) cuando el backend corre con AUTH_ENABLED=true. */
  readonly VITE_API_KEY?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
