import { xmipAdminApi } from '@/lib/xmipAdminApi'
import type {
  AgentRunnerSummary,
  AuditSummary,
  BlockerItem,
  ConnectorsSummary,
  DashboardOverview,
  EditorialWorkQueueItem,
  FrontendConfig,
  IntakeQueueItem,
  NewsroomHealth,
  OperationalAuditEvent,
  OperationalGap,
  OwnershipBoard,
  PublicationBoardItem,
  ReadinessBoardItem,
  ReadyResponse,
  RouteMapGroup,
  TaskBoardItem,
} from '@/types/xmip'

export const adminApi = {
  getReady: (signal?: AbortSignal) => xmipAdminApi.get<ReadyResponse>('/ready', signal),
  getFrontendConfig: (signal?: AbortSignal) =>
    xmipAdminApi.get<FrontendConfig>('/api/v1/admin/frontend/config', signal),
  getRouteMap: (signal?: AbortSignal) =>
    xmipAdminApi.get<RouteMapGroup[]>('/api/v1/admin/frontend/route-map', signal),
  getDashboardOverview: (signal?: AbortSignal) =>
    xmipAdminApi.get<DashboardOverview>('/api/v1/admin/dashboard/overview', signal),
  getNewsroomHealth: (signal?: AbortSignal) =>
    xmipAdminApi.get<NewsroomHealth>('/api/v1/admin/dashboard/newsroom-health', signal),
  getIntakeQueue: (signal?: AbortSignal) =>
    xmipAdminApi.get<IntakeQueueItem[]>('/api/v1/admin/intake/queue?limit=8', signal),
  getEditorialWorkQueue: (signal?: AbortSignal) =>
    xmipAdminApi.get<EditorialWorkQueueItem[]>('/api/v1/admin/editorial/work-queue?limit=8', signal),
  getBlockers: (signal?: AbortSignal) =>
    xmipAdminApi.get<BlockerItem[]>('/api/v1/admin/blockers?limit=8', signal),
  getReadinessBoard: (signal?: AbortSignal) =>
    xmipAdminApi.get<ReadinessBoardItem[]>('/api/v1/admin/readiness/board?limit=8', signal),
  getTaskBoard: (signal?: AbortSignal) =>
    xmipAdminApi.get<TaskBoardItem[]>('/api/v1/admin/tasks/board?limit=8', signal),
  getPublicationBoard: (signal?: AbortSignal) =>
    xmipAdminApi.get<PublicationBoardItem[]>('/api/v1/admin/publications/board?limit=8', signal),
  getOwnershipBoard: (signal?: AbortSignal) =>
    xmipAdminApi.get<OwnershipBoard>('/api/v1/admin/ownership/board', signal),
  getOperationalGaps: (signal?: AbortSignal) =>
    xmipAdminApi.get<OperationalGap[]>('/api/v1/admin/gaps', signal),
  getAgentRunnerSummary: (signal?: AbortSignal) =>
    xmipAdminApi.get<AgentRunnerSummary>('/api/v1/admin/agent-runner/summary', signal),
  getConnectorsSummary: (signal?: AbortSignal) =>
    xmipAdminApi.get<ConnectorsSummary>('/api/v1/admin/connectors/summary', signal),
  getAuditSummary: (signal?: AbortSignal) =>
    xmipAdminApi.get<AuditSummary>('/api/v1/admin/audit/summary', signal),
  // Registro de auditoría operacional (RBAC: requiere sesión HttpOnly con
  // permiso operational_audit.read). Distinto de los audit checks públicos.
  getOperationalAuditEvents: (signal?: AbortSignal) =>
    xmipAdminApi.get<OperationalAuditEvent[]>('/api/v1/operational-audit/events?limit=25', signal),
}
