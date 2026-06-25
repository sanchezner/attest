from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.dependencies import get_db
from db.queries import upsert_contract
from db.schemas import Contract

router = APIRouter(prefix='/api/v1/projects', tags=['contracts'])


@router.post('/{project_slug}/contracts', status_code=201)
def register_contract(
    project_slug: str,
    contract: Contract,
    db: Session = Depends(get_db),
):
    row = upsert_contract(db, project_slug, contract)
    return {
        'id': row.id,
        'project_slug': project_slug,
        'artifact_id': row.artifact_id,
    }


@router.post('/{project_slug}/contracts/bulk', status_code=201)
def register_contracts_bulk(
    project_slug: str,
    contracts: list[Contract],
    db: Session = Depends(get_db),
):
    results = []
    for contract in contracts:
        row = upsert_contract(db, project_slug, contract)
        results.append({'id': row.id, 'artifact_id': row.artifact_id})
    return {'registered': len(results), 'contracts': results}