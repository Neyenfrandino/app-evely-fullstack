from app.db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, LargeBinary
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime

class User(Base):
    __tablename__ = 'user'
    id= Column(Integer, primary_key = True, autoincrement = True )
    pastillas_tabla_id= Column(Integer, ForeignKey('pastillas_tabla.id', ondelete='CASCADE'), nullable=True)
    name= Column(String, nullable=False)
    last_name=Column(String, nullable=False)
    username= Column(String, nullable=False, unique= True)
    password= Column(String, nullable=False)
    birth_date= Column(Date, nullable=False)
    date_creation = Column(DateTime, default= datetime.now, onupdate=datetime.now)
    profile_photo= Column(LargeBinary)
    email= Column(String, nullable=False, unique= True)
    nationalidad= Column(String)

    pastillas_tabla_relation = relationship('Pastillas_tabla', backref='user_relation', cascade='delete,merge')


class Pastillas_tabla(Base):
    __tablename__= 'pastillas_tabla'
    id = Column(Integer, primary_key = True, autoincrement = True)
    # user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    name = Column(String, nullable= False)
    description = Column(String)
    number_of_tablet_pills = Column(Integer)    

    user = relationship('User', backref='pastillas_tabla', cascade='delete,merge')


class Datos_usuario_pastilla(Base):
    __tablename__ = 'datos_usuario_pastilla'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    pastilla_id = Column(Integer, ForeignKey('pastillas_tabla.id', ondelete='CASCADE'), nullable=False)
    initial_treatment = Column(Date, nullable=False)
    finish_treatment = Column(Date)
    frequency_takes = Column(String)
    last_take = Column(String)
    current_date = Column(DateTime)
    

