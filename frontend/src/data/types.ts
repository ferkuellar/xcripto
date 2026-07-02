export type Priority = 'P0' | 'P1' | 'P2' | 'P3' | 'P4'

export type RiskLevel = 'critical' | 'high' | 'medium' | 'low' | 'unknown'

export type VerificationStatus =
  | 'verified'
  | 'partially_verified'
  | 'rumor'
  | 'monitoring'
  | 'unverified'
  | 'rejected'

export type AgentStatus = 'idle' | 'running' | 'waiting_review' | 'blocked' | 'completed'

export type PipelineStage =
  | 'detected'
  | 'validating'
  | 'risk_review'
  | 'drafting'
  | 'reviewing'
  | 'approved'
  | 'scheduled'
  | 'published'

export type AgentMode = 'A0' | 'A1' | 'A2' | 'A3' | 'A4'

export interface NewsItem {
  id: string
  title: string
  category: string
  priority: Priority
  verification: VerificationStatus
  risk: RiskLevel
  source: string
  agent: string
  timestamp: string
  stage: PipelineStage
  missing: string[]
}

export interface Signal {
  id: string
  title: string
  category: string
  priority: Priority
  source: string
  sourceStatus: 'active' | 'flagged' | 'blocked'
  duplicate: boolean
  discarded: boolean
  detectedAt: string
}

export interface Agent {
  id: string
  name: string
  status: AgentStatus
  lastRun: string
  currentTask: string
  outputCount: number
  mode: AgentMode
  avgRuntime: string
  description: string
}

export interface SourceRecord {
  id: string
  name: string
  type: string
  trust: 'T0' | 'T1' | 'T2' | 'T3' | 'T4' | 'T5'
  evidence: 'E0' | 'E1' | 'E2' | 'E3' | 'E4' | 'E5'
  confidence: 'C0' | 'C1' | 'C2' | 'C3' | 'C4' | 'C5'
  status: 'active' | 'under_review' | 'flagged' | 'blocked'
  lastChecked: string
  linkedItems: number
}

export interface RiskItem {
  id: string
  title: string
  level: RiskLevel
  severity: 'S1' | 'S2' | 'S3' | 'S4'
  recommendation: string
  disclaimers: string[]
  blocked: boolean
  humanReview: boolean
  relatedNewsId: string
}

export interface VerificationItem {
  id: string
  title: string
  status: VerificationStatus
  sources: number
  confidence: string
  agent: string
  updatedAt: string
}

export interface PipelineAlert {
  id: string
  type:
    | 'missing_source'
    | 'missing_verification'
    | 'missing_risk_review'
    | 'missing_approval'
    | 'rumor_as_fact'
    | 'blocked_source'
  message: string
  itemRef: string
  severity: 'critical' | 'high' | 'medium'
}

export type ContentType =
  | 'Brief'
  | 'Article'
  | 'Video Script'
  | 'Short'
  | 'Thread'
  | 'Newsletter'

export interface ContentPiece {
  id: string
  type: ContentType
  title: string
  owner: string
  status: 'draft' | 'in_review' | 'approved' | 'blocked' | 'scheduled'
  channel: string
  progress: number
  reviewPending: boolean
}

export interface ScheduledPublication {
  id: string
  channel: string
  title: string
  time: string
  day: string
  status: 'ready' | 'pending_deps' | 'blocked' | 'published'
  missingDeps: string[]
  risk: RiskLevel
  expectedMetric: string
}

export interface AuditCheck {
  id: string
  name: string
  status: 'pass' | 'fail' | 'warning'
  detail: string
  correlationId: string
  itemRef: string
}

export interface GraphNode {
  id: string
  label: string
  type: string
  x: number
  y: number
}

export interface GraphEdge {
  from: string
  to: string
  relation: string
}

export interface MemoryItem {
  id: string
  type: 'editorial_rule' | 'source_pattern' | 'incident_lesson' | 'style_preference'
  content: string
  createdBy: string
  reinforcedCount: number
  createdAt: string
}

export interface Notification {
  id: string
  title: string
  detail: string
  time: string
  kind: 'risk' | 'agent' | 'publication' | 'system'
  unread: boolean
}

export interface Kpi {
  id: string
  label: string
  value: number
  deltaPct: number
  state: 'good' | 'warning' | 'critical' | 'neutral'
  icon: string
}
