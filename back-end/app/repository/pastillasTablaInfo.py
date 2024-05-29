# Aqui van las funciones de usuario para hacer el crud 
from app.db import models
from fastapi import HTTPException, status


def create_pastilla_info(user_id, schema, db):
    infoSchema = dict(schema)
    user_true = db.query(models.User).filter(models.User.id == user_id).first()
    print(user_true.id)

    if not user_true:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Dont exist user {user_id}')

    
    try:
        newInfo = models.Pastillas_tabla(
            # user_id = user_true.id,
            name = infoSchema['name'],
            description = infoSchema['description']
        )

        db.add(newInfo)
        db.commit()
        db.refresh(newInfo)
        return {'Message': 'Successfully create data'}
    except Exception as e :
        raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail= f'Error create user {e}')
    

def get_data_pastillas_tabla_info_all_user(user_id, db):
    user_true = db.query(models.User).filter(models.User.id == user_id).first()

 
    if not user_true:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Dont exist user {user_id}')
    
    data_user_true = db.query(models.Pastillas_tabla).filter(models.Pastillas_tabla.id == models.Datos_usuario_pastilla.pastilla_id).filter(models.Datos_usuario_pastilla.user_id == user_true.id).all()

    print(data_user_true)
 

    return data_user_true

def get_pastillas_tabla_all(user_id, db):
    user_true = db.query(models.User).filter(models.User.id == user_id).first()
 
    if not user_true:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Dont exist user {user_id}')

    data_user_pills_all = db.query(models.Pastillas_tabla).all()
    print(data_user_pills_all)

    return data_user_pills_all

def update_pastilla_tabla_info(user_id, number_entry, schema, db ):
    user_true = db.query(models.User).filter(models.User.id == user_id).first()

    if not user_true:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Dont exist user {user_id}')
    
    lista_data  = db.query(models.Pastillas_tabla).filter(models.Pastillas_tabla.id == number_entry).first()

    if not lista_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Error, entry not found {number_entry}')
    
    schema_dict = dict(schema)


    new_data = {
        'name': schema_dict.get('name', lista_data.name),
        'description': schema_dict.get('description', lista_data.description)
    }

    for key, value in new_data.items():
        setattr(lista_data, key, value)

    db.commit()

    return{'Message': 'data update successfully'}

def delete_data_pastilla_tabla(user_id, number_entry, db):
    user_true = db.query(models.User).filter(models.User.id == user_id).first()

    if not user_true:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f'Dont exist user {user_id}')
    
    lista_data = db.query(models.Pastillas_tabla).filter(models.Pastillas_tabla.id == number_entry).first()

    if not lista_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Error, entry not found {number_entry}')
    
    db.delete(lista_data)
    db.commit()
    return{'Message': 'data deleted successfully'}

