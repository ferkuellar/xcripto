import { xmipAdminApi } from '@/lib/xmipAdminApi'
import type { AuthLoginResponse, AuthMeResponse } from '@/types/xmip'

export const authApi = {
  login: (identifier: string, password: string) =>
    xmipAdminApi.post<AuthLoginResponse>('/api/v1/auth/login', {
      identifier,
      password,
    }),
  me: (signal?: AbortSignal) => xmipAdminApi.get<AuthMeResponse>('/api/v1/auth/me', signal),
  logout: () => xmipAdminApi.post<void>('/api/v1/auth/logout'),
}
