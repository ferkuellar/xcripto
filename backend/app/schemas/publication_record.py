from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.constants import DISTRIBUTION_CHANNELS, PUBLICATION_STATUSES


class PublicationRecordBase(BaseModel):
    content_piece_id: str = Field(min_length=1, max_length=80)
    distribution_plan_id: str = Field(min_length=1, max_length=80)
    news_item_id: str = Field(min_length=1, max_length=80)
    channel: str
    publication_status: str = "scheduled"
    published_url: str | None = Field(default=None, max_length=2048)
    external_id: str | None = Field(default=None, max_length=180)
    published_at: datetime | None = None
    owner: str | None = Field(default=None, max_length=120)
    notes: str | None = None
    correlation_id: str | None = Field(default=None, max_length=80)

    @field_validator("channel")
    @classmethod
    def validate_channel(cls, value: str) -> str:
        if value not in DISTRIBUTION_CHANNELS:
            raise ValueError(f"channel must be one of {sorted(DISTRIBUTION_CHANNELS)}")
        return value

    @field_validator("publication_status")
    @classmethod
    def validate_publication_status(cls, value: str) -> str:
        if value not in PUBLICATION_STATUSES:
            raise ValueError(f"publication_status must be one of {sorted(PUBLICATION_STATUSES)}")
        return value


class PublicationRecordCreate(PublicationRecordBase):
    pass


class PublicationRecordStatusUpdate(BaseModel):
    publication_status: str

    @field_validator("publication_status")
    @classmethod
    def validate_publication_status(cls, value: str) -> str:
        if value not in PUBLICATION_STATUSES:
            raise ValueError(f"publication_status must be one of {sorted(PUBLICATION_STATUSES)}")
        return value


class PublicationRecordRead(PublicationRecordBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime
