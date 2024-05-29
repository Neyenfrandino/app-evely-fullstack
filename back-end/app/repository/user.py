# Aqui van las funciones de usuario para hacer el crud 
from app.db import models
from fastapi import HTTPException, status
from app.hashing import Hash

def create_user(user, db):
    new_user = dict(user)
    try:
        user_new = models.User(
            name = new_user['name'],
            last_name = new_user['last_name'],
            username = new_user['username'],
            password = Hash.hash_password(new_user['password']),
            birth_date = new_user['birth_date'],
            profile_photo = new_user['profile_photo'],
            email = new_user['email'],
            nationalidad = new_user['nationalidad'],
        )

        db.add(user_new)
        db.commit()
        db.refresh(user_new)
        return {'Message': 'usuario creado exitosamente'}
    except Exception as e :
        raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail= f'Error crear usuario {e}')
    
 
def get_usera_all(user_id, db):
    user = db.query(models.User).filter(models.User.id == user_id).all()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'No existe el usuario con el id {user_id}')
    return user 

def delete_user(user_id, db):
    user_delete = db.query(models.User).filter(models.User.id == user_id).first()

    if not user_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'No existe el usuario con el id {user_id}')

    db.delete(user_delete)

    db.commit()	
    return{'Respuesta': 'El usuario a sido eliminado correctamente'}

def update_user(user_id, schema, db):
    print('si entro aqui ')

    user_update = db.query(models.User).filter(models.User.id == user_id)

    if not user_update.first():
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'El usuario con el id {user_id} no ha sido encontrado')
    
    new_values = {}

    for i, e in dict(schema).items():
        if e != None:
            new_values[i] = e

    user_update.update(new_values)
    db.commit()
    return{'Respuesta':'El usuario ha sido modificado correctamente'}
