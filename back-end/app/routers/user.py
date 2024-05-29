from app.schemas import User, User_id, Update_user
from fastapi import APIRouter, Depends
from app.db.database import get_db
from sqlalchemy.orm import Session	
from app.oauth import get_current_user


from app.repository import user


router = APIRouter(prefix="/user",
                   tags=["Users"])

@router.get('/')
def holmundo():
    return 'hola mundo '

@router.post('/create_user')
def create_user(user_schema: User, db: Session = Depends(get_db)):
    response = user.create_user(user_schema, db)
    return response

@router.get('/get_user/{user_id}')
def get_usera_all(user_id : int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user) ):
    response = user.get_usera_all(user_id, db)
    return response

@router.delete('/delete_user/{user_id}')
def delete_user(user_id: int, db : Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    response = user.delete_user(user_id, db)
    return response


@router.patch('/update_user/{user_id}')
def update_user(user_id : int, schema_update: Update_user, db : Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    response = user.update_user(user_id, schema_update, db)
    return response