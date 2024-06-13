from fastapi import APIRouter, Depends, status
from app.db.database import get_db
from sqlalchemy.orm import Session
from typing import List
from app.repository import auth
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix='/login',
                   tags=['Login'])


@router.post('/', status_code=status.HTTP_200_OK)
def login(usuario:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    auth_token = auth.auth_user(usuario, db)
    return auth_token

    
@router.post("/img")
async def upload_image(imageData: dict, db: Session = Depends(get_db)):
    received_text = imageData.get("imageData")
    response = auth.compare_images(received_text, db)

    return response
    
    