from app.schemas import  User, PastillasTablaInfo
from fastapi import APIRouter, Depends
from app.db.database import get_db
from sqlalchemy.orm import Session	
from app.oauth import get_current_user
from app.repository import data_user_pills_filter_tablet_all


router = APIRouter(prefix="/data_user_pills_filter_tablet_all",
                   tags=["Data_user_pills_filter_tablet_all"])


@router.get('/data_user_pills_filter_tablet_all/{user_id}')
def dataUserPillsFilterTabletAll(user_id: int , db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    response = data_user_pills_filter_tablet_all.data_user_pills_filter_tablet_all(user_id, db)
    return response