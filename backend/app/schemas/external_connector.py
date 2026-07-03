from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.core.constants import (
    EXTERNAL_CONNECTOR_AUTH_TYPES,
    EXTERNAL_CONNECTOR_CAPABILITIES,
    EXTERNAL_CONNECTOR_RUN_STATUSES,
    EXTERNAL_CONNECTOR_RUN_TYPES,
    EXTERNAL_CONNECTOR_SECRET_KEYS,
    EXTERNAL_CONNECTOR_STATUSES,
    EXTERNAL_CONNECTOR_TYPES,
)


def contains_secret_key(value: Any) -> bool:
    if isinstance(value, dict):
        for key, nested_value in value.items():
            normalized_key = str(key).strip().lower()
            if normalized_key in EXTERNAL_CONNECTOR_SECRET_KEYS:
                return True
            if contains_secret_key(nested_value):
                return True
    if isinstance(value, list):
        return any(contains_secret_key(item) for item in value)
    return False


class ExternalConnectorBase(BaseModel):
    connector_name: str = Field(min_length=1, max_length=160)
    connector_type: str
    connector_status: str = "draft"
    provider: str | None = Field(default=None, max_length=120)
    base_url: str | None = Field(default=None, max_length=2048)
    description: str | None = None
    capabilities: list[str] = Field(default_factory=list)
    configuration: dict[str, Any] | list[Any] | None = None
    secret_ref: str | None = Field(default=None, max_length=240)
    auth_type: str = "none"
    rate_limit_policy: dict[str, Any] | list[Any] | None = None
    enabled: bool = False
    dry_run_only: bool = True
    correlation_id: str | None = Field(default=None, max_length=80)

    @field_validator("connector_type")
    @classmethod
    def validate_connector_type(cls, value: str) -> str:
        if value not in EXTERNAL_CONNECTOR_TYPES:
            raise ValueError(f"connector_type must be one of {sorted(EXTERNAL_CONNECTOR_TYPES)}")
        return value

    @field_validator("connector_status")
    @classmethod
    def validate_connector_status(cls, value: str) -> str:
        if value not in EXTERNAL_CONNECTOR_STATUSES:
            raise ValueError(
                f"connector_status must be one of {sorted(EXTERNAL_CONNECTOR_STATUSES)}"
            )
        return value

    @field_validator("auth_type")
    @classmethod
    def validate_auth_type(cls, value: str) -> str:
        if value not in EXTERNAL_CONNECTOR_AUTH_TYPES:
            raise ValueError(f"auth_type must be one of {sorted(EXTERNAL_CONNECTOR_AUTH_TYPES)}")
        return value

    @field_validator("capabilities")
    @classmethod
    def validate_capabilities(cls, value: list[str]) -> list[str]:
        invalid = sorted(set(value) - EXTERNAL_CONNECTOR_CAPABILITIES)
        if invalid:
            raise ValueError(f"capabilities contain unsupported values: {invalid}")
        return value

    @model_validator(mode="after")
    def validate_configuration_safety(self) -> "ExternalConnectorBase":
        if self.enabled and not self.dry_run_only:
            raise ValueError("External connectors must remain dry_run_only in this phase")
        return self


class ExternalConnectorCreate(ExternalConnectorBase):
    pass


class ExternalConnectorUpdate(BaseModel):
    connector_name: str | None = Field(default=None, min_length=1, max_length=160)
    connector_type: str | None = None
    connector_status: str | None = None
    provider: str | None = Field(default=None, max_length=120)
    base_url: str | None = Field(default=None, max_length=2048)
    description: str | None = None
    capabilities: list[str] | None = None
    configuration: dict[str, Any] | list[Any] | None = None
    secret_ref: str | None = Field(default=None, max_length=240)
    auth_type: str | None = None
    rate_limit_policy: dict[str, Any] | list[Any] | None = None
    enabled: bool | None = None
    dry_run_only: bool | None = None

    @field_validator("connector_type")
    @classmethod
    def validate_connector_type(cls, value: str | None) -> str | None:
        if value is not None and value not in EXTERNAL_CONNECTOR_TYPES:
            raise ValueError(f"connector_type must be one of {sorted(EXTERNAL_CONNECTOR_TYPES)}")
        return value

    @field_validator("connector_status")
    @classmethod
    def validate_connector_status(cls, value: str | None) -> str | None:
        if value is not None and value not in EXTERNAL_CONNECTOR_STATUSES:
            raise ValueError(
                f"connector_status must be one of {sorted(EXTERNAL_CONNECTOR_STATUSES)}"
            )
        return value

    @field_validator("auth_type")
    @classmethod
    def validate_auth_type(cls, value: str | None) -> str | None:
        if value is not None and value not in EXTERNAL_CONNECTOR_AUTH_TYPES:
            raise ValueError(f"auth_type must be one of {sorted(EXTERNAL_CONNECTOR_AUTH_TYPES)}")
        return value

    @field_validator("capabilities")
    @classmethod
    def validate_capabilities(cls, value: list[str] | None) -> list[str] | None:
        if value is None:
            return value
        invalid = sorted(set(value) - EXTERNAL_CONNECTOR_CAPABILITIES)
        if invalid:
            raise ValueError(f"capabilities contain unsupported values: {invalid}")
        return value

    @model_validator(mode="after")
    def validate_configuration_safety(self) -> "ExternalConnectorUpdate":
        if self.enabled is True and self.dry_run_only is False:
            raise ValueError("External connectors must remain dry_run_only in this phase")
        return self


class ExternalConnectorRead(ExternalConnectorBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    last_run_at: datetime | None = None
    last_success_at: datetime | None = None
    last_failure_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class ExternalConnectorRunBase(BaseModel):
    connector_id: str | None = None
    run_type: str = "dry_run"
    run_status: str = "created"
    triggered_by: str | None = Field(default=None, max_length=120)
    input_payload: dict[str, Any] | list[Any] | None = None
    result_payload: dict[str, Any] | list[Any] | None = None
    signals_created_count: int = Field(default=0, ge=0)
    agent_outputs_created_count: int = Field(default=0, ge=0)
    publication_records_created_count: int = Field(default=0, ge=0)
    metric_snapshots_created_count: int = Field(default=0, ge=0)
    error_message: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    correlation_id: str | None = Field(default=None, max_length=80)

    @field_validator("run_type")
    @classmethod
    def validate_run_type(cls, value: str) -> str:
        if value not in EXTERNAL_CONNECTOR_RUN_TYPES:
            raise ValueError(f"run_type must be one of {sorted(EXTERNAL_CONNECTOR_RUN_TYPES)}")
        return value

    @field_validator("run_status")
    @classmethod
    def validate_run_status(cls, value: str) -> str:
        if value not in EXTERNAL_CONNECTOR_RUN_STATUSES:
            raise ValueError(
                f"run_status must be one of {sorted(EXTERNAL_CONNECTOR_RUN_STATUSES)}"
            )
        return value


class ExternalConnectorRunCreate(ExternalConnectorRunBase):
    connector_id: str


class ExternalConnectorDryRunRequest(BaseModel):
    run_type: str = "dry_run"
    input_payload: dict[str, Any] | list[Any] | None = None
    triggered_by: str | None = Field(default=None, max_length=120)

    @field_validator("run_type")
    @classmethod
    def validate_run_type(cls, value: str) -> str:
        if value not in EXTERNAL_CONNECTOR_RUN_TYPES:
            raise ValueError(f"run_type must be one of {sorted(EXTERNAL_CONNECTOR_RUN_TYPES)}")
        return value


class ExternalConnectorRunRead(ExternalConnectorRunBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    connector_id: str
    created_at: datetime
    updated_at: datetime


class ExternalConnectorContractValidation(BaseModel):
    passed: bool
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    connector_id: str


class ExternalConnectorDryRunResponse(BaseModel):
    connector: ExternalConnectorRead
    run: ExternalConnectorRunRead
    validation: ExternalConnectorContractValidation


class AdminConnectorRunItem(BaseModel):
    id: str
    connector_id: str
    run_type: str
    run_status: str
    created_at: datetime
    completed_at: datetime | None = None


class AdminConnectorsSummary(BaseModel):
    total_connectors: int
    enabled_connectors: int
    dry_run_only_connectors: int
    connectors_by_type: dict[str, int]
    connectors_by_status: dict[str, int]
    recent_connector_runs: list[AdminConnectorRunItem]
    failed_connector_runs: int
