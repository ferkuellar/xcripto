from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.core.constants import (
    KNOWLEDGE_CONFIDENCE_LEVELS,
    KNOWLEDGE_NODE_TYPES,
    KNOWLEDGE_RELATIONSHIP_TYPES,
    KNOWLEDGE_SCOPES,
    KNOWLEDGE_STATUSES,
)


class KnowledgeNodeBase(BaseModel):
    node_type: str
    label: str = Field(min_length=1, max_length=280)
    external_ref: str | None = Field(default=None, max_length=180)
    entity_type: str | None = Field(default=None, max_length=80)
    entity_id: str | None = Field(default=None, max_length=80)
    description: str | None = None
    confidence_level: str = "KC2"
    status: str = "proposed"
    source_or_origin: str = Field(min_length=1)
    metadata_json: dict | list | None = Field(
        default=None, validation_alias="metadata", serialization_alias="metadata"
    )
    correlation_id: str | None = Field(default=None, max_length=80)

    @field_validator("node_type")
    @classmethod
    def validate_node_type(cls, value: str) -> str:
        if value not in KNOWLEDGE_NODE_TYPES:
            raise ValueError(f"node_type must be one of {sorted(KNOWLEDGE_NODE_TYPES)}")
        return value

    @field_validator("confidence_level")
    @classmethod
    def validate_confidence_level(cls, value: str) -> str:
        if value not in KNOWLEDGE_CONFIDENCE_LEVELS:
            raise ValueError(
                f"confidence_level must be one of {sorted(KNOWLEDGE_CONFIDENCE_LEVELS)}"
            )
        return value

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        if value not in KNOWLEDGE_STATUSES:
            raise ValueError(f"status must be one of {sorted(KNOWLEDGE_STATUSES)}")
        return value

    @model_validator(mode="after")
    def validate_relation(self) -> "KnowledgeNodeBase":
        if (self.entity_type and not self.entity_id) or (self.entity_id and not self.entity_type):
            raise ValueError("entity_type and entity_id must be provided together")
        return self


class KnowledgeNodeCreate(KnowledgeNodeBase):
    pass


class KnowledgeNodeRead(KnowledgeNodeBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime


class KnowledgeEdgeBase(BaseModel):
    source_node_id: str = Field(min_length=1, max_length=80)
    target_node_id: str = Field(min_length=1, max_length=80)
    relationship_type: str
    scope: str
    confidence_level: str = "KC2"
    reason: str = Field(min_length=1)
    status: str = "proposed"
    risk_flags: list[str] = Field(default_factory=list)
    metadata_json: dict | list | None = Field(
        default=None, validation_alias="metadata", serialization_alias="metadata"
    )
    correlation_id: str | None = Field(default=None, max_length=80)

    @field_validator("relationship_type")
    @classmethod
    def validate_relationship_type(cls, value: str) -> str:
        if value not in KNOWLEDGE_RELATIONSHIP_TYPES:
            raise ValueError(
                f"relationship_type must be one of {sorted(KNOWLEDGE_RELATIONSHIP_TYPES)}"
            )
        return value

    @field_validator("scope")
    @classmethod
    def validate_scope(cls, value: str) -> str:
        if value not in KNOWLEDGE_SCOPES:
            raise ValueError(f"scope must be one of {sorted(KNOWLEDGE_SCOPES)}")
        return value

    @field_validator("confidence_level")
    @classmethod
    def validate_confidence_level(cls, value: str) -> str:
        if value not in KNOWLEDGE_CONFIDENCE_LEVELS:
            raise ValueError(
                f"confidence_level must be one of {sorted(KNOWLEDGE_CONFIDENCE_LEVELS)}"
            )
        return value

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        if value not in KNOWLEDGE_STATUSES:
            raise ValueError(f"status must be one of {sorted(KNOWLEDGE_STATUSES)}")
        return value

    @model_validator(mode="after")
    def validate_nodes(self) -> "KnowledgeEdgeBase":
        if self.source_node_id == self.target_node_id:
            raise ValueError("KnowledgeEdge cannot point to itself")
        return self


class KnowledgeEdgeCreate(KnowledgeEdgeBase):
    pass


class KnowledgeEdgeRead(KnowledgeEdgeBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime


class KnowledgeEntityGraphRead(BaseModel):
    nodes: list[KnowledgeNodeRead] = Field(default_factory=list)
    edges: list[KnowledgeEdgeRead] = Field(default_factory=list)
