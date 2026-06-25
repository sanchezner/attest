from datetime import datetime
import time
from sqlalchemy import DateTime, Integer, String, Boolean, Float, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ObservationRow(Base):
    __tablename__ = 'observations'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_slug: Mapped[str] = mapped_column(String(64), index=True)
    artifact_id: Mapped[str] = mapped_column(String(256), index=True)
    reporter: Mapped[str] = mapped_column(String(64))
    row_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ContractRow(Base):
    __tablename__ = 'contracts'
    __table_args__ = (
        UniqueConstraint('project_slug', 'artifact_id', name='uq_project_artifact'),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_slug: Mapped[str] = mapped_column(String(64), index=True)
    artifact_id: Mapped[str] = mapped_column(String(256), index=True)
    min_row_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    max_age_hours: Mapped[float | None] = mapped_column(Float, nullable=True)
    must_exist: Mapped[bool] = mapped_column(Boolean, default=False)
    expected_reporter: Mapped[str | None] = mapped_column(String(64), nullable=True)


class ReporterTokenRow(Base):
    __tablename__ = 'reporter_tokens'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_slug: Mapped[str] = mapped_column(String(64), index=True)
    reporter: Mapped[str] = mapped_column(String(64))
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)


class EvaluationRow(Base):
    __tablename__ = 'evaluations'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_slug: Mapped[str] = mapped_column(String(64), index=True)
    artifact_id: Mapped[str] = mapped_column(String(256), index=True)
    status: Mapped[str] = mapped_column(String(16))
    reason: Mapped[str | None] = mapped_column(String(512), nullable=True)
    evaluated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


class AlertLogRow(Base):
    __tablename__ = 'alert_log'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_slug: Mapped[str] = mapped_column(String(64), index=True)
    artifact_id: Mapped[str] = mapped_column(String(256), index=True)
    previous_status: Mapped[str | None] = mapped_column(String(16), nullable=True)
    current_status: Mapped[str | None] = mapped_column(String(16))
    reason: Mapped[str | None] = mapped_column(String(512), nullable=True)
    ntfy_topic: Mapped[str] = mapped_column(String(128))
    http_status: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sent_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    