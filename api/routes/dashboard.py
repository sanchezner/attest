from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.dependencies import get_db
from db.schemas import ProjectStatus
from evaluator.status import get_artifact_statuses

router = APIRouter(prefix='/api/v1/projects', tags=['dashboard'])


@router.get('/{project_slug}/dashboard/status', response_model=ProjectStatus)
def dashboard_status(
    project_slug: str,
    artifact_id: str | None = None,
    db: Session = Depends(get_db),
):
    now = datetime.now(timezone.utc)
    artifacts = get_artifact_statuses(
        session=db,
        project_slug=project_slug,
        now=now,
        artifact_id=artifact_id,
    )

    if artifact_id is not None and not artifacts:
        raise HTTPException(status_code=404, detail='contract not found')

    return ProjectStatus(
        project_slug=project_slug,
        evaluated_at=now,
        artifacts=artifacts,
    )