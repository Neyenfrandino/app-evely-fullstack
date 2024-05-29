from app.schemas import Create_datos_usuario_pastilla, Update_datos_usuario_pastilla, User
from fastapi import APIRouter, Depends
from app.db.database import get_db
from sqlalchemy.orm import Session	
from app.oauth import get_current_user
from app.repository import datos_usuario_pastilla


router = APIRouter(prefix="/datos_usuario_pastilla",
                   tags=["Datos_usuario_pastilla"])

@router.post('/create_data/{user_id}')
def create_data_usuario_pastilla(user_id : int, schema : Create_datos_usuario_pastilla , db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    response = datos_usuario_pastilla.create_datos_usuario_pastilla(user_id, schema, db)
    return response


@router.get('/get_data/{user_id}')
def get_data(user_id : int, db : Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    response = datos_usuario_pastilla.get_data_all(user_id, db)
    return response


@router.patch('/update_datos_pastilla_usuario/{user_id}/{id_update_data}')
def update_datos_pastillas_usuario(user_id: int, id_update_data: int, schema: Update_datos_usuario_pastilla, db : Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    response = datos_usuario_pastilla.update_datos_pastillas_usuario(user_id, id_update_data, schema, db)
    return response


