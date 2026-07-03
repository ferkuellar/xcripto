/**
 * Contratos del backend XMIP (FastAPI, /api/v1).
 * Espejo de backend/app/schemas/*. No inventar campos aquí:
 * si el backend cambia un schema, este archivo es el único punto a actualizar.
 */

export type NewsPriority = 'P0' | 'P1' | 'P2' | 'P3' | 'P4'

export type NewsStatus =
  | 'detected'
  | 'registered'
  | 'classified'
  | 'validating'
  | 'verified'
  | 'partially_verified'
  | 'rumor'
  | 'monitoring'
  | 'rejected'
  | 'prioritized'
  | 'drafting'
  | 'reviewing'
  | 'approved'
  | 'scheduled'
  | 'published'
  | 'distributed'
  | 'measured'
  | 'archived'
  | 'corrected'
  | 'retracted'
  | 'escalated'

export interface HealthResponse {
  status: string
  service: string
  version: string
}

export interface NewsRead {
  id: string
  title: string
  summary: string
  category: string
  priority: NewsPriority
  status: NewsStatus
  source_url: string
  source_name: string
  correlation_id: string | null
  created_at: string
  updated_at: string
}

export interface SourceRead {
  id: string
  source_name: string
  source_url: string
  source_type: string
  source_status:
    | 'proposed'
    | 'active'
    | 'trusted'
    | 'watchlist'
    | 'restricted'
    | 'blocked'
    | 'archived'
  trust_level: string
  notes: string | null
  correlation_id: string | null
  created_at: string
  updated_at: string
}

export interface SourceCreate {
  source_name: string
  source_url: string
  source_type: string
  source_status?: SourceRead['source_status']
  trust_level?: string
  notes?: string | null
}

export interface AgentExecutionRead {
  id: string
  agent_name: string
  agent_version: string
  input_ref: string | null
  output_ref: string | null
  status: string
  started_at: string | null
  completed_at: string | null
  error_message: string | null
  correlation_id: string | null
  created_at: string
  updated_at: string
}

export interface AuditCheckRead {
  id: string
  entity_type: string
  entity_id: string
  audit_status: 'pass' | 'fail' | 'warning' | 'pending'
  severity: 'low' | 'medium' | 'high' | 'critical'
  decision_recommendation: string | null
  ready_to_advance: boolean
  publication_block_recommended: boolean
  missing_requirements: string[]
  audit_flags: string[]
  correlation_id: string | null
  created_at: string
  updated_at: string
}

export interface IntakeSignalRead {
  id: string
  signal_type: string
  signal_status: string
  source_name: string | null
  source_url: string | null
  source_type: string | null
  source_published_at: string | null
  raw_title: string | null
  raw_summary: string | null
  normalized_title: string | null
  normalized_summary: string | null
  language: string | null
  topic: string | null
  asset_symbols: string[]
  entities: string[]
  keywords: string[]
  priority: NewsPriority
  confidence_level: string
  risk_flags: string[]
  adapter_name: string | null
  duplicate_of_signal_id: string | null
  linked_news_item_id: string | null
  promoted_news_item_id: string | null
  dedupe_status: string
  dedupe_score: number | null
  content_hash: string
  dedupe_key: string
  correlation_id: string | null
  created_at: string
  updated_at: string
}

export interface IntakeSignalCreate {
  signal_type?: string
  source_name?: string
  source_url?: string
  raw_title: string
  raw_summary?: string
  priority?: NewsPriority
  topic?: string
}

export interface NewsCreate {
  title: string
  summary: string
  category: string
  priority?: NewsPriority
  source_url: string
  source_name: string
}
