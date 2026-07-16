export interface ApiErrorPayload {
  status: number
  message: string
  correlationId: string | null
}

export interface AuthUser {
  id: string
  email: string | null
  display_name: string
  handle: string | null
  role: string
  roles: string[]
  is_active: boolean
  last_login_at: string | null
}

export interface AuthSessionInfo {
  session_expires_at: string
  authenticated: boolean
}

export interface AuthLoginResponse {
  user: AuthUser
  session: AuthSessionInfo
}

export interface AuthMeResponse {
  authenticated: boolean
  user: AuthUser
  session: AuthSessionInfo
}

export interface ReadyResponse {
  status: 'ready' | 'not_ready' | string
  service: string
  version: string
  checks: Record<string, string>
}

export interface FrontendConfig {
  app_name: string
  app_version: string
  environment: string
  auth_enabled: boolean
  rbac_enabled: boolean
  features: Record<string, boolean>
  required_headers: string[]
}

export interface RouteMapItem {
  label: string
  path: string
  method: string
  permission: string | null
  frontend_section: string
}

export interface RouteMapGroup {
  group: string
  routes: RouteMapItem[]
}

export interface DashboardOverview {
  total_news: number
  total_intake_signals: number
  pending_intake_signals: number
  duplicate_intake_signals: number
  promoted_intake_signals: number
  active_workflows: number
  blocked_workflows: number
  pending_tasks: number
  blocked_tasks: number
  completed_tasks: number
  latest_readiness_count: number
  ready_to_advance_count: number
  blocked_readiness_count: number
  published_records_count: number
  scheduled_publications_count: number
  pending_agent_reviews_count: number
  active_users_count: number
  unassigned_news_count: number
  unassigned_tasks_count: number
}

export interface NewsroomHealth {
  health_status: string
  health_score: number
  critical_blockers: string[]
  warnings: string[]
  recommended_actions: string[]
  counts_by_news_status: Record<string, number>
  counts_by_workflow_status: Record<string, number>
  counts_by_task_status: Record<string, number>
  counts_by_readiness_status: Record<string, number>
}

export interface IntakeQueueItem {
  signal_id: string
  raw_title: string | null
  normalized_title: string | null
  source_name: string | null
  source_url: string | null
  signal_status: string
  dedupe_status: string
  priority: string
  confidence_level: string
  duplicate_of_signal_id: string | null
  promoted_news_item_id: string | null
  created_at: string
}

export interface EditorialWorkQueueItem {
  news_item_id: string
  title: string
  status: string
  priority: string
  workflow_run_id: string | null
  current_step: string | null
  readiness_status: string | null
  score: number | null
  missing_requirements: string[]
  blocking_reasons: string[]
  next_agent: string | null
  recommended_next_action: string | null
  pending_task_count: number
  blocking_task_count: number
  owner: string | null
  created_at: string
  updated_at: string
}

export interface BlockerItem {
  blocker_type: string
  entity_type: string
  entity_id: string
  news_item_id: string | null
  title_or_summary: string
  reason: string
  severity: string
  recommended_action: string
  created_at: string
}

export interface ReadinessBoardItem {
  news_item_id: string
  title: string
  score: number
  score_band: string
  readiness_status: string
  human_review_required: boolean
  publication_block_recommended: boolean
  missing_requirements: string[]
  warnings: string[]
  blocking_reasons: string[]
  next_agent: string | null
  recommended_next_action: string | null
  calculated_at: string
}

export interface TaskBoardItem {
  task_id: string
  workflow_run_id: string
  news_item_id: string | null
  title: string
  task_type: string
  task_status: string
  priority: string
  assigned_agent: string | null
  assigned_to: string | null
  blocking: boolean
  blocking_reason: string | null
  attempt_count: number
  max_attempts: number
  due_at: string | null
  created_at: string
  updated_at: string
}

export interface PublicationBoardItem {
  publication_record_id: string
  news_item_id: string | null
  content_piece_id: string | null
  distribution_plan_id: string | null
  title: string
  channel: string
  publication_status: string
  published_url: string | null
  external_id: string | null
  published_at: string | null
  owner: string | null
  created_at: string
  updated_at: string
}

export interface OwnershipBoardUser {
  user_id: string
  display_name: string
  role: string
  active_assignment_count: number
  active_task_count: number
  owned_news_count: number
  review_items_count: number
}

export interface OwnershipBoard {
  users: OwnershipBoardUser[]
  assignments: unknown[]
  unassigned_news: unknown[]
  unassigned_tasks: unknown[]
  unassigned_content_pieces: unknown[]
}

export interface OperationalGap {
  gap_type: string
  count: number
  severity: string
  recommended_action: string
  sample_entity_ids: string[]
}

export interface AgentRunnerSummary {
  total_internal_runs: number
  completed_runs: number
  failed_runs: number
  outputs_pending_review: number
  tasks_eligible_for_runner: number
  recent_runs: unknown[]
}

export interface ConnectorsSummary {
  total_connectors: number
  enabled_connectors: number
  dry_run_only_connectors: number
  connectors_by_type: Record<string, number>
  connectors_by_status: Record<string, number>
  recent_connector_runs: unknown[]
  failed_connector_runs: number
}

export interface AuditSummary {
  total_events: number
  events_by_type: Record<string, number>
  events_by_outcome: Record<string, number>
  events_by_decision: Record<string, number>
  recent_events: unknown[]
}

/**
 * Evento del registro de auditoría operacional
 * (`GET /api/v1/operational-audit/events`, protegido por RBAC).
 * Distinto de un Audit Check editorial (`/api/v1/audit/checks`): esto registra
 * quién hizo qué en el backend (actor, outcome, decisión) para trazabilidad.
 * Campos opcionales por tolerancia a variaciones menores del read model.
 */
export interface OperationalAuditEvent {
  id: string
  event_type: string
  action: string | null
  permission: string | null
  outcome: string
  decision: string | null
  actor_id: string | null
  actor_role: string | null
  entity_type: string | null
  entity_id: string | null
  reason: string | null
  error_message: string | null
  correlation_id: string | null
  created_at: string
}
