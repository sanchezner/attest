from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.dependencies import get_db, require_reporter
from db.schemas import ProjectStatus
from evaluator.status import get_artifact_statuses

router = APIRouter(prefix='/api/v1/projects', tags=['status'])


@router.get('/{project_slug}/status', response_model=ProjectStatus)
def project_status(
    project_slug: str,
    artifact_id: str | None = None,
    db: Session = Depends(get_db),
    auth: tuple[str, str] = Depends(require_reporter),
):
    auth_project, _auth_reporter = auth
    
    if auth_project != project_slug:
        raise HTTPException(status_code=403, detail='token not valid for this project')
    
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