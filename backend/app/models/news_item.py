from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin


class NewsItem(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "news_items"

    title: Mapped[str] = mapped_column(String(280), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(80), nullable=False)
    priority: Mapped[str] = mapped_column(String(2), nullable=False, default="P3", index=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="detected", index=True)
    source_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    source_name: Mapped[str] = mapped_column(String(180), nullable=False)
    cover_image_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    correlation_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)

