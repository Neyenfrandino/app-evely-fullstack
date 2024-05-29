from app.schemas import  User, PastillasTablaInfo
from fastapi import APIRouter, Depends
from app.db.database import get_db
from sqlalchemy.orm import Session	
from app.oauth import get_current_user
from app.repository import pastillasTablaInfo


router = APIRouter(prefix="/pastillaTablaInfo",
                   tags=["PastillaTablaInfo"])

@router.post('/create_data/{user_id}')
def create_data_usuario_pastilla(user_id : int, schema: PastillasTablaInfo, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    response = pastillasTablaInfo.create_pastilla_info(user_id, schema, db)
    return response


@router.get('/get_data_pastillas_tabla_info_all_user/{user_id}')
def get_data_all_user(user_id: int , db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    response =  pastillasTablaInfo.get_data_pastillas_tabla_info_all_user(user_id, db )
    return response

@router.get('/get_data_all/{user_id}')
def get_data_all(user_id: int , db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    response =  pastillasTablaInfo.get_pastillas_tabla_all(user_id, db )
    return response

@router.patch('/update_tabla_pastilla/{user_id}/{number_entry}')
def update_pastilla_tabla_info(user_id, number_entry: int, schema: PastillasTablaInfo, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    response = pastillasTablaInfo.update_pastilla_tabla_info(user_id, number_entry, schema, db)
    return response

@router.delete('delete_data/{user_id}/{number_entry}')
def delete_data_pastilla_tabla(user_id: int, number_entry: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user) ):
    response = pastillasTablaInfo.delete_data_pastilla_tabla(user_id, number_entry, db)
    return response