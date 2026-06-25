from collections.abc import Generator
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from db.session import SessionLocal
from db.queries import get_reporter_for_token

bearer_scheme = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def require_reporter(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    db: Session = Depends(get_db),
):
    result = get_reporter_for_token(db, credentials.credentials)
    if result is None:
        raise HTTPException(status_code=401, detail='invalid token')
    return result