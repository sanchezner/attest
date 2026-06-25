from sqlalchemy import select
from sqlalchemy.orm import Session
from db.models import ObservationRow, ContractRow, ReporterTokenRow, EvaluationRow, AlertLogRow
from db.schemas import Observation, Contract, EvaluationStatus, EvaluationResult
from db.auth import hash_token
from datetime import datetime


def get_latest_observation(
    session: Session,
    project_slug: str,
    artifact_id: str,
):
    stmt = (
        select(ObservationRow)
        .where(
            ObservationRow.project_slug == project_slug,
            ObservationRow.artifact_id == artifact_id,
        )
        .order_by(ObservationRow.observed_at.desc())
        .limit(1)
    )
    row = session.scalar(stmt)
    if row is None:
        return None

    return Observation(
        artifact_id=row.artifact_id,
        reporter=row.reporter,
        observed_at=row.observed_at,
        row_count=row.row_count,
    )


def insert_observation(
    session: Session,
    project_slug: str,
    observation: Observation,
):
    row = ObservationRow(
        project_slug=project_slug,
        artifact_id=observation.artifact_id,
        reporter=observation.reporter,
        row_count=observation.row_count,
        observed_at=observation.observed_at,
    )
    session.add(row)
    session.commit()
    session.refresh(row)
    return row


def upsert_contract(
    session: Session,
    project_slug: str,
    contract: Contract,
):
    stmt = (
        select(ContractRow)
        .where(
            ContractRow.project_slug == project_slug,
            ContractRow.artifact_id ==  contract.artifact_id,
        )
    )
    row = session.scalar(stmt)
    if row is None:
        row = ContractRow(project_slug=project_slug)
        session.add(row)

    row.artifact_id = contract.artifact_id
    row.min_row_count = contract.min_row_count
    row.max_age_hours = contract.max_age_hours
    row.must_exist = contract.must_exist
    row.expected_reporter = contract.expected_reporter

    session.commit()
    session.refresh(row)
    return row


def _contract_from_row(row: ContractRow):
    return Contract(
        artifact_id=row.artifact_id,
        min_row_count=row.min_row_count,
        max_age_hours=row.max_age_hours,
        must_exist=row.must_exist,
        expected_reporter=row.expected_reporter,
    )


def get_contracts_for_project(
    session: Session,
    project_slug: str,
):
    stmt = (
        select(ContractRow)
        .where(
            ContractRow.project_slug == project_slug
        )
    )
    rows = session.scalars(stmt).all()
    return [_contract_from_row(row) for row in rows]


def get_reporter_for_token(
    session: Session,
    token: str,
):
    token_hash = hash_token(token)
    stmt = (
        select(ReporterTokenRow)
        .where(
            ReporterTokenRow.token_hash == token_hash
        )
    )
    row = session.scalar(stmt)
    if row is None:
        return None
    return row.project_slug, row.reporter


def list_all_contracts(session: Session):
    stmt = select(ContractRow)
    rows = session.scalars(stmt).all()
    return [(row.project_slug, _contract_from_row(row)) for row in rows]


def get_latest_evaluation_status(
    session: Session,
    project_slug: str,
    artifact_id: str,
):
    stmt = (
        select(EvaluationRow)
        .where(
            EvaluationRow.project_slug == project_slug,
            EvaluationRow.artifact_id == artifact_id,
        )
        .order_by(EvaluationRow.evaluated_at.desc())
        .limit(1)
    )
    row = session.scalar(stmt)
    if row is None:
        return None
    return EvaluationStatus(row.status)


def insert_evaluation(
    session: Session,
    project_slug: str,
    artifact_id: str,
    result: EvaluationResult,
    *,
    evaluated_at: datetime | None = None,
):
    row = EvaluationRow(
        project_slug=project_slug,
        artifact_id=artifact_id,
        status=result.status.value,
        reason=result.reason,
    )
    if evaluated_at is not None:
        row.evaluated_at = evaluated_at
    session.add(row)
    session.commit()
    session.refresh(row)
    return row


def insert_alert_log(
    session: Session,
    project_slug: str,
    artifact_id: str,
    *,
    previous_status: str | None,
    current_status: str,
    reason: str | None,
    ntfy_topic: str,
    http_status: int | None,
    sent_at: datetime | None = None,
):
    row = AlertLogRow(
        project_slug=project_slug,
        artifact_id=artifact_id,
        previous_status=previous_status,
        current_status=current_status,
        reason=reason,
        ntfy_topic=ntfy_topic,
        http_status=http_status,
    )
    if sent_at is not None:
        row.sent_at = sent_at
    session.add(row)
    session.commit()
    session.refresh(row)
    return row