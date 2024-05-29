# Aqui vamos a definir los modelos en que vamos a recibir los datos. 

from pydantic import BaseModel 
from typing import Optional, Union
from datetime import datetime, date

class User(BaseModel):
    name: str
    last_name: str
    username: str
    password: str
    birth_date : date
    date_creation : datetime = datetime.now()
    profile_photo: Optional[bytes] = None
    email: str
    nationalidad: Optional[str] = None

class User_id(BaseModel):
    id: int


class Update_user(BaseModel):
    name: str = None
    last_name: str = None
    username: str = None
    password: str = None
    birth_date : date = None
    date_creation : datetime = datetime.now()
    profile_photo: Optional[bytes] = None
    email: str = None
    nationalidad: Optional[str] = None


class Create_datos_usuario_pastilla(BaseModel):
    # user_id: int = None
    pastilla_id : int = None
    initial_treatment : date = None
    finish_treatment : Optional[date] = None
    frequency_takes : Optional[str] = None
    last_take : Optional[date] = None
    current_date : datetime


class Update_datos_usuario_pastilla(BaseModel):
    initial_treatment: Optional[date] = None
    finish_treatment: Optional[date] = None
    frequency_takes: Optional[str] = None
    last_take: Optional[str] = None
    current_date: Optional[datetime] = None
    number_of_tablet_pills: Optional[int] = None
    

class Login(BaseModel):
    username : str
    password : str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None    


class PastillasTablaInfo(BaseModel):
    name: str
    description: str


