from datetime import datetime, timezone
from sqlalchemy.orm import Session
from db.queries import get_contracts_for_project, get_latest_observation
from db.schemas import ArtifactStatus
from evaluator.contract import evaluate_contract


def get_artifact_statuses(
    session: Session,
    project_slug: str,
    *,
    now: datetime | None = None,
    artifact_id: str | None = None,
):
    if now is None:
        now = datetime.now(timezone.utc)

    contracts = get_contracts_for_project(session, project_slug)
    if artifact_id is not None:
        contracts = [c for c in contracts if c.artifact_id == artifact_id]

    statuses = []
    for contract in contracts:
        latest = get_latest_observation(session, project_slug, contract.artifact_id)
        result = evaluate_contract(contract, latest, now=now)
        statuses.append(
            ArtifactStatus(
                artifact_id=contract.artifact_id,
                status=result.status,
                reason=result.reason,
                observed_at=latest.observed_at if latest else None,
            )
        )
    return statuses