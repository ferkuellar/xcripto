from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.constants import RISK_DECISION_RECOMMENDATIONS, RISK_LEVELS, RISK_SEVERITIES


class RiskReviewBase(BaseModel):
    news_item_id: str = Field(min_length=1, max_length=80)
    entity_type: str = Field(min_length=2, max_length=80)
    entity_id: str = Field(min_length=1, max_length=80)
    risk_level: str = "unknown"
    severity: str = "R-SEV-1"
    decision_recommendation: str
    risk_flags: list[str] = Field(default_factory=list)
    summary: str = Field(min_length=1)
    required_disclaimers: list[str] = Field(default_factory=list)
    language_restrictions: list[str] = Field(default_factory=list)
    human_review_required: bool = False
    publication_block_recommended: bool = False
    reviewer: str | None = Field(default=None, max_length=120)
    correlation_id: str | None = Field(default=None, max_length=80)

    @field_validator("risk_level")
    @classmethod
    def validate_risk_level(cls, value: str) -> str:
        if value not in RISK_LEVELS:
            raise ValueError(f"risk_level must be one of {sorted(RISK_LEVELS)}")
        return value

    @field_validator("severity")
    @classmethod
    def validate_severity(cls, value: str) -> str:
        if value not in RISK_SEVERITIES:
            raise ValueError(f"severity must be one of {sorted(RISK_SEVERITIES)}")
        return value

    @field_validator("decision_recommendation")
    @classmethod
    def validate_decision_recommendation(cls, value: str) -> str:
        if value not in RISK_DECISION_RECOMMENDATIONS:
            raise ValueError(
                f"decision_recommendation must be one of {sorted(RISK_DECISION_RECOMMENDATIONS)}"
            )
        return value


class RiskReviewCreate(RiskReviewBase):
    pass


class RiskReviewRead(RiskReviewBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime
