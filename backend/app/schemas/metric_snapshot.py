from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.core.constants import METRIC_CATEGORIES, METRIC_DATA_QUALITIES, METRIC_MEASUREMENT_WINDOWS


class MetricSnapshotBase(BaseModel):
    entity_type: str | None = Field(default=None, max_length=80)
    entity_id: str | None = Field(default=None, max_length=80)
    news_item_id: str | None = Field(default=None, max_length=80)
    content_piece_id: str | None = Field(default=None, max_length=80)
    distribution_plan_id: str | None = Field(default=None, max_length=80)
    publication_record_id: str | None = Field(default=None, max_length=80)
    workflow_run_id: str | None = Field(default=None, max_length=80)
    workflow_task_id: str | None = Field(default=None, max_length=80)
    agent_execution_id: str | None = Field(default=None, max_length=80)
    agent_output_id: str | None = Field(default=None, max_length=80)
    metric_category: str
    channel: str | None = Field(default=None, max_length=120)
    measurement_window: str
    metric_name: str = Field(min_length=1, max_length=120)
    metric_value: float
    snapshot_payload: dict | list | None = None
    source_or_origin: str = Field(min_length=1)
    data_quality: str
    notes: str | None = None
    correlation_id: str | None = Field(default=None, max_length=80)

    @field_validator("metric_category")
    @classmethod
    def validate_metric_category(cls, value: str) -> str:
        if value not in METRIC_CATEGORIES:
            raise ValueError(f"metric_category must be one of {sorted(METRIC_CATEGORIES)}")
        return value

    @field_validator("measurement_window")
    @classmethod
    def validate_measurement_window(cls, value: str) -> str:
        if value not in METRIC_MEASUREMENT_WINDOWS:
            raise ValueError(
                f"measurement_window must be one of {sorted(METRIC_MEASUREMENT_WINDOWS)}"
            )
        return value

    @field_validator("data_quality")
    @classmethod
    def validate_data_quality(cls, value: str) -> str:
        if value not in METRIC_DATA_QUALITIES:
            raise ValueError(f"data_quality must be one of {sorted(METRIC_DATA_QUALITIES)}")
        return value

    @model_validator(mode="after")
    def validate_relations(self) -> "MetricSnapshotBase":
        if (self.entity_type and not self.entity_id) or (self.entity_id and not self.entity_type):
            raise ValueError("entity_type and entity_id must be provided together")
        return self


class MetricSnapshotCreate(MetricSnapshotBase):
    pass


class MetricSnapshotRead(MetricSnapshotBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime
