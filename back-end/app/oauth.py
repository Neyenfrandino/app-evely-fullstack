from fastapi import Depends, HTTPException, status
from app.token import verify_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')


def get_current_user(token: Annotated[str, Depends(oauth2_schema)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    return verify_token(token, credentials_exception)