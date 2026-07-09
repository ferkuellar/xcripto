from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class PublicNewsRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    slug: str
    title: str
    summary: str
    category: str
    source_name: str
    source_url: str
    status: str
    author: str | None = None
    published_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
    cover_image_url: str | None = None
    tags: list[str] = Field(default_factory=list)
    canonical_url: str
    seo_title: str
    seo_description: str
    og_title: str
    og_description: str
    og_image: str | None = None
    json_ld_type: str = "NewsArticle"


class PublicArticleRead(PublicNewsRead):
    body: str
    body_format: Literal["markdown", "html", "plain"] = "markdown"
