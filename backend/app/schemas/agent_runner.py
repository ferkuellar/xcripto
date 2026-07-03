from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.schemas.agent_execution import AgentExecutionRead
from app.schemas.agent_output import AgentOutputRead
from app.schemas.workflow_task import WorkflowTaskRead


class AgentCapability(BaseModel):
    agent_name: str
    supported_task_types: list[str]
    output_type: str
    internal_only: bool = True
    external_integrations: bool = False
    description: str


class AgentRunnerTaskEligibility(BaseModel):
    eligible: bool
    reason: str | None = None
    task_id: str
    task_status: str
    task_type: str
    assigned_agent: str
    recommended_agent: str | None = None
    output_type: str | None = None


class AgentRunnerDryRunResponse(BaseModel):
    task_id: str
    eligible: bool
    reason: str | None = None
    recommended_agent: str | None = None
    output_type: str | None = None
    payload_preview: dict[str, Any]


class AgentRunnerRunRequest(BaseModel):
    force: bool = False
    runner: str = Field(default="internal", max_length=40)


class AgentRunnerRunResponse(BaseModel):
    status: str
    task: WorkflowTaskRead
    execution: AgentExecutionRead
    output: AgentOutputRead


class AgentRunnerWorkflowRunNextRequest(BaseModel):
    force: bool = False
    runner: str = Field(default="internal", max_length=40)


class AgentRunnerWorkflowRunNextResponse(BaseModel):
    status: str
    workflow_run_id: str
    message: str | None = None
    result: AgentRunnerRunResponse | None = None


class AgentRunnerRecentRunItem(BaseModel):
    id: str
    agent_name: str
    agent_version: str
    input_ref: str | None
    output_ref: str | None
    status: str
    started_at: datetime | None
    completed_at: datetime | None
    error_message: str | None
    correlation_id: str | None
    created_at: datetime


class AdminAgentRunnerSummary(BaseModel):
    total_internal_runs: int
    completed_runs: int
    failed_runs: int
    outputs_pending_review: int
    tasks_eligible_for_runner: int
    recent_runs: list[AgentRunnerRecentRunItem]
