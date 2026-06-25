from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum

class Contract(BaseModel):
    artifact_id: str = Field(
        ...,
        description='Logical artifact path',
        examples=['bronze/gamelogs'],
    )
    min_row_count: int | None = Field(
        default=None,
        ge=0,
        description='Minimum rows required; None = don\'t check row count',
    )
    max_age_hours: float | None = Field(
        default=None,
        gt=0,
        description='Max hours since last observation; None = don\'t check freshness',
    )
    must_exist: bool = Field(
        default=False,
        description='If True, any observation proves existence',
    )
    expected_reporter: str | None = Field(
        default=None,
        description='Which worker should report this'
    )

class Observation(BaseModel):
    artifact_id: str = Field(
        ...,
        description='Logical artifact path',
        examples=['bronze/gamelogs'],
    )
    reporter: str = Field(
        ...,
        description='Worker identity',
    )
    observed_at: datetime = Field(
        ...,
        description='When the worker finished (UTC)',
    )
    row_count: int | None = Field(
        default=None,
        ge=0,
        description='Rows written; None if only checking existence',
    )


class EvaluationStatus(str, Enum):
    OK = 'ok'
    VIOLATED = 'violated'
    MISSING = 'missing'


class EvaluationResult(BaseModel):
    status: EvaluationStatus
    reason: str | None = None


class ArtifactStatus(BaseModel):
    artifact_id: str
    status: EvaluationStatus
    reason: str | None = None
    observed_at: datetime | None = None


class ProjectStatus(BaseModel):
    project_slug: str
    evaluated_at: datetime
    artifacts: list[ArtifactStatus]