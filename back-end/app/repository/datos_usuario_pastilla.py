# Aqui van las funciones de usuario para hacer el crud 
from app.db import models
from fastapi import HTTPException, status

def create_datos_usuario_pastilla(user_id, schema, db):
    user_true = db.query(models.User).filter(models.User.id == user_id).first()

    if not user_true:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'No existe el usuario con el id {user_id}')
    
    try:
        new_values = models.Datos_usuario_pastilla(
            user_id= user_true.id,
            pastilla_id = schema.pastilla_id,
            initial_treatment=schema.initial_treatment,
            finish_treatment=schema.finish_treatment,
            frequency_takes=schema.frequency_takes,
            last_take=schema.last_take,
            current_date=schema.current_date
        )

        db.add(new_values)
        db.commit()
        db.refresh(new_values)
        return {'Message': 'Successfully create data'}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'Error al crear los datos del usuario: {e}')
    

def get_data_all(user_id, db):
    user_true = db.query(models.User).filter(models.User.id == user_id).first()

    if not user_true:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f'No existe el usuario con el id {user_id}')
    

    data_pastillas_user = db.query(models.Datos_usuario_pastilla).filter(models.Datos_usuario_pastilla.user_id == user_true.id).all()
    return data_pastillas_user

def update_datos_pastillas_usuario(user_id, id_update_data, schema, db):
    user_true = db.query(models.User).filter(models.User.id == user_id).first() 
    
    if not user_true:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'No existe el usuario con el id {user_id}')
    
    filter_id_data_update = db.query(models.Datos_usuario_pastilla).filter(models.Datos_usuario_pastilla.id == id_update_data).first()

    if not filter_id_data_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'No existe los datos {id_update_data}')

    # Actualizar los atributos del objeto con los valores del esquema
    for field, value in schema:
        setattr(filter_id_data_update, field, value)

    db.commit()
    return {'Message': 'Los datos fueron modificados corretamente'}


