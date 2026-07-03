from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.constants import EDITORIAL_READINESS_SCORE_BANDS, EDITORIAL_READINESS_STATUSES


class EditorialReadinessScoreBase(BaseModel):
    news_item_id: str = Field(min_length=1, max_length=80)
    workflow_run_id: str | None = Field(default=None, max_length=80)
    score: float = Field(ge=0, le=100)
    score_band: str
    readiness_status: str
    source_score: float = Field(ge=0, le=100)
    verification_score: float = Field(ge=0, le=100)
    risk_score: float = Field(ge=0, le=100)
    editorial_score: float = Field(ge=0, le=100)
    audit_score: float = Field(ge=0, le=100)
    workflow_score: float = Field(ge=0, le=100)
    task_score: float = Field(ge=0, le=100)
    agent_output_score: float = Field(ge=0, le=100)
    distribution_score: float = Field(ge=0, le=100)
    publication_score: float = Field(ge=0, le=100)
    metrics_score: float = Field(ge=0, le=100)
    memory_score: float = Field(ge=0, le=100)
    knowledge_score: float = Field(ge=0, le=100)
    blocking_reasons: list[str] = Field(default_factory=list)
    missing_requirements: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    recommended_next_action: str | None = None
    next_agent: str = "None"
    human_review_required: bool = False
    publication_block_recommended: bool = False
    score_payload: dict = Field(default_factory=dict)
    calculated_by: str = "system"
    correlation_id: str | None = Field(default=None, max_length=80)

    @field_validator("score_band")
    @classmethod
    def validate_score_band(cls, value: str) -> str:
        if value not in EDITORIAL_READINESS_SCORE_BANDS:
            raise ValueError(
                f"score_band must be one of {sorted(EDITORIAL_READINESS_SCORE_BANDS)}"
            )
        return value

    @field_validator("readiness_status")
    @classmethod
    def validate_readiness_status(cls, value: str) -> str:
        if value not in EDITORIAL_READINESS_STATUSES:
            raise ValueError(
                f"readiness_status must be one of {sorted(EDITORIAL_READINESS_STATUSES)}"
            )
        return value


class EditorialReadinessScoreRead(EditorialReadinessScoreBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime
