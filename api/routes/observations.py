from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.dependencies import get_db, require_reporter
from db.queries import insert_observation
from db.schemas import Observation

router = APIRouter(prefix='/api/v1/projects', tags=['observations'])

@router.post('/{project_slug}/observations', status_code=201)
def create_observation(
    project_slug: str,
    observation: Observation,
    db: Session = Depends(get_db),
    auth: tuple[str, str] = Depends(require_reporter),
):
    auth_project, auth_reporter = auth

    if auth_project != project_slug:
        raise HTTPException(status_code=403, detail='token not valid for this project')

    if observation.reporter != auth_reporter:
        raise HTTPException(status_code=403, detail='reporter mismatch')

    row = insert_observation(db, project_slug, observation)
    return {
        'id': row.id,
        'project_slug': project_slug,
        'artifact_id': row.artifact_id,
        'received_at': row.received_at,
    }

