from sqlalchemy.orm import Session
from app.db import models
from fastapi import HTTPException, status
from app.hashing import Hash
from app.token import create_access_token

def auth_user(usuario, db):
    user_true = db.query(models.User).filter(models.User.username == usuario.username).first()
    print(user_true.password, 'jaja')
    if not user_true:   
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Dont exits user {usuario.username}')
    
    if not Hash.verify_password(usuario.password, user_true.password):
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Contraseña incorrecta')
    
    access_token = create_access_token(
        data={'sub': user_true.username}
    )

    user_data = db.query(models.Datos_usuario_pastilla, models.User, models.Pastillas_tabla).\
        select_from(models.Datos_usuario_pastilla).\
        join(models.User, models.Datos_usuario_pastilla.user_id == models.User.id).\
        join(models.Pastillas_tabla, models.Datos_usuario_pastilla.pastilla_id == models.Pastillas_tabla.id).\
        filter(models.Datos_usuario_pastilla.user_id == user_true.id).all()

    # user_data_dict = {}
  
    # for datos_usuario_pastilla, user, pastillas_tabla in user_data:
       
    #     user_data_dict[datos_usuario_pastilla.id] = {
             
    #     'datos_usuario_pastilla': {
    #         'id': datos_usuario_pastilla.id,
    #         'pastilla_id_user': datos_usuario_pastilla.pastilla_id,
    #         'initial_treatment': datos_usuario_pastilla.initial_treatment,
    #         'finish_treatment': datos_usuario_pastilla.finish_treatment,
    #         'frequency_takes': datos_usuario_pastilla.frequency_takes,
    #         'last_take': datos_usuario_pastilla.last_take,
    #         'current_date': datos_usuario_pastilla.current_date
    #     },

    #     'pastillas_tabla': {
    #         'id': pastillas_tabla.id,
    #         'name': pastillas_tabla.name,
    #         'description': pastillas_tabla.description,
    #         'number_of_tablet_pills': pastillas_tabla.number_of_tablet_pills
    #     }
    # }
        
    # usuario = {
    #         'id': user_true.id,
    #         'name': user_true.name,
    #         'username': user_true.username,  
    #         'email': user_true.email,  
    #         'photo_profile': user_true.profile_photo, 
    #         'nationality': user_true.nationalidad, 
    #         'birth_date': user_true.birth_date
    # },


    return {
        'access_token': access_token, 
        'token_type': 'bearer', 
        'user_true': user_true.id, 
    }
