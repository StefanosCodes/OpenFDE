import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.settings import Settings, get_settings

bearer = HTTPBearer(auto_error=False)


def require_service_key(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> None:
    expected = settings.nexus_api_key.get_secret_value()
    supplied = credentials.credentials if credentials and credentials.scheme == "Bearer" else ""
    if not supplied or not secrets.compare_digest(supplied, expected):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Valid service authentication is required.",
            headers={"WWW-Authenticate": "Bearer"},
        )
