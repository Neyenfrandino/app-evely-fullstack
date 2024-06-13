from app.db import models
from fastapi import HTTPException, status
from sqlalchemy.orm import aliased
import json
import base64

def data_user_pills_filter_tablet_all(user_id, db):
    user_true = db.query(models.User).filter(models.User.id == user_id).first()
    if not user_true:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No existe el usuario con el id {user_id}'
        )

    try:
        Usuario = aliased(models.User)
        DatosUsuarioPastilla = aliased(models.Datos_usuario_pastilla)
        PastillasTabla = aliased(models.Pastillas_tabla)

        data_user_tablet = db.query(
            Usuario, DatosUsuarioPastilla, PastillasTabla
        ).join(
            DatosUsuarioPastilla, Usuario.id == DatosUsuarioPastilla.user_id
        ).join(
            PastillasTabla, DatosUsuarioPastilla.pastilla_id == PastillasTabla.id
        ).filter(
            Usuario.id == user_true.id
        ).all()

        result = {
            "usuario": None,
            "datos_usuario_pastilla": [],
            "pastillas": []
        }

        if data_user_tablet:
            for usuario, datos_usuario_pastilla, pastillas_tabla in data_user_tablet:
                if result["usuario"] is None:
                    result["usuario"] = {
                        "id": usuario.id,
                        "name": usuario.name,
                        "last_name": usuario.last_name,
                        "username": usuario.username,
                        "password": usuario.password,
                        "birth_date": usuario.birth_date.strftime('%Y-%m-%d') if usuario.birth_date else None,
                        "date_creation": usuario.date_creation.strftime('%Y-%m-%d') if usuario.date_creation else None,
                        "profile_photo": base64.b64encode(usuario.profile_photo).decode('utf-8') if usuario.profile_photo else None,
                        "email": usuario.email,
                        "nationality": usuario.nationalidad if usuario.nationalidad else None
                    }

                result["datos_usuario_pastilla"].append({
                    "id": datos_usuario_pastilla.id,
                    "user_id": datos_usuario_pastilla.user_id,
                    "pastilla_id": datos_usuario_pastilla.pastilla_id,
                    "initial_treatment": datos_usuario_pastilla.initial_treatment.strftime('%Y-%m-%d') if datos_usuario_pastilla.initial_treatment else None,
                    "finish_treatment": datos_usuario_pastilla.finish_treatment.strftime('%Y-%m-%d') if datos_usuario_pastilla.finish_treatment else None,
                    "frequency_takes": datos_usuario_pastilla.frequency_takes if datos_usuario_pastilla.frequency_takes else None,
                    "last_take": datos_usuario_pastilla.last_take if datos_usuario_pastilla.last_take else None,
                    "current_date": datos_usuario_pastilla.current_date.strftime('%Y-%m-%d %H:%M:%S') if datos_usuario_pastilla.current_date else None
                })

                result["pastillas"].append({
                    "id": pastillas_tabla.id,
                    "name": pastillas_tabla.name,
                    "description": pastillas_tabla.description,
                    'number_of_tablet_pills': pastillas_tabla.number_of_tablet_pills
                })

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontraron datos."
            )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Error al crear los datos del usuario: {e}'
        )
