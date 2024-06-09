from sqlalchemy.orm import Session
from app.db import models
from fastapi import HTTPException, status
from app.hashing import Hash
from app.token import create_access_token

import cv2
import face_recognition as fr
import os
import numpy as np
import base64
from io import BytesIO
from PIL import Image
import io
import time


def auth_user(usuario, db):
    user_true = db.query(models.User).filter(models.User.username == usuario.username).first()
  
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


    return {
        'access_token': access_token, 
        'token_type': 'bearer', 
        'user_true': user_true.id, 
    }




def resize_image(image, size=(500, 500)):
    return cv2.resize(image, size)


def decode_base64_image(file):
    try:
        # Remover encabezados de diferentes tipos de imágenes base64
        if "data:image/jpeg;base64," in file:
            base64_data = file.replace("data:image/jpeg;base64,", "")
        elif "data:image/png;base64," in file:
            base64_data = file.replace("data:image/png;base64,", "")
        elif "data:image/webp;base64," in file:
            base64_data = file.replace("data:image/webp;base64,", "")
        else:
            raise ValueError("Formato de imagen no soportado")

        # Decodificar la cadena Base64
        image_data = base64.b64decode(base64_data)
        # Crear un objeto de flujo de bytes
        image_stream = io.BytesIO(image_data)
        # Abrir la imagen usando Pillow
        imagen_pillow = Image.open(image_stream)
        # Convertir la imagen a un arreglo de numpy
        imagen = np.array(imagen_pillow)
        return imagen
    except Exception as e:
        print(f"Error al decodificar la imagen base64: {e}")
        return None
    
# Caché para imágenes decodificadas
decode_cache = {}

def decode_base64_image_cached(file):
    if file in decode_cache:
        return decode_cache[file]

    imagen = decode_base64_image(file)
    decode_cache[file] = imagen

    return imagen

def codificar(imagenes):
    lista_codificada = []

    for imagen in imagenes:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        codificado = fr.face_encodings(imagen)[0]
        lista_codificada.append(codificado)

    return lista_codificada

def get_user(user_all):

    mis_imagenes = []

    for user in user_all:
        imagen = user.profile_photo
        photo = imagen.decode('utf-8')  # Convierte los bytes a una cadena UTF-8

        if "data:image/jpeg;base64," in photo:
            base64_data = photo.replace("data:image/jpeg;base64,", "")
        elif "data:image/png;base64," in photo:
            base64_data = photo.replace("data:image/png;base64,", "")
        elif "data:image/webp;base64," in photo:
            base64_data = photo.replace("data:image/webp;base64,", "")
        else:
            raise ValueError("Formato de imagen no soportado: {}".format(photo[:50]))  # Muestra los primeros 50 caracteres de la cadena 'imagen'

        if not base64_data:

            print(f"La ruta de la foto de perfil es nula o vacía para el usuario")
            continue

        # Decodificar la cadena Base64 en bytes
        image_data = base64.b64decode(base64_data)

        # Crear un objeto de imagen a partir de los bytes decodificados
        image = Image.open(BytesIO(image_data))

        # Guardar la imagen en un archivo
        image.save('imagen_decodificada.jpg', 'JPEG')
        # Redimensionar la imagen si se decodificó correctamente

        image_np = np.array(image)
        imagen_actual = {'imagen': resize_image(image_np), 'id': user.id}
        mis_imagenes.append(imagen_actual)

    return mis_imagenes

def compare_images(file, db):
    user_all = db.query(models.User).all()

    start_time = time.time()  # Guardar el tiempo antes de ejecutar las funciones

    imagen = decode_base64_image_cached(file)
    if imagen is None:
        return "Error al decodificar la imagen base64."

    mis_imagenes = get_user(user_all)

    imagenes = [imagen['imagen'] for imagen in mis_imagenes]

     
    if not imagenes:
        return "No se encontraron imágenes de los usuarios."

    lista_empleados_codificada = codificar(imagenes)

    cara_captura = fr.face_locations(imagen)
    if not cara_captura:
        return "No se detectó ninguna cara en la imagen proporcionada."

    # Codificar cara capturada
    cara_captura_codificada = fr.face_encodings(np.array(imagen), cara_captura)

    for caracodif, caraubic in zip(cara_captura_codificada, cara_captura):
        coincidencias = fr.compare_faces(lista_empleados_codificada, caracodif)
        distancias = fr.face_distance(lista_empleados_codificada, caracodif)

        indice_coincidencia = np.argmin(distancias)

        if distancias[indice_coincidencia] > 0.6:
            return "No coincide con ninguno de nuestros empleados"
        else:
            # Obtener el id del usuario que coincide
            user_id = mis_imagenes[indice_coincidencia]['id']
            # Usar el id para obtener más información del usuario si es necesario
            usuario = db.query(models.User).filter(models.User.id == user_id).first()

            if not usuario:   
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Dont exits user {usuario.username}')
            
            access_token = create_access_token(
                data={'sub': usuario.username}
            )
            return {
                'access_token': access_token, 
                # 'token_type': 'bearer', 
                'user_true': usuario.id, 
            }
    elapsed_time = time.time() - start_time  # Calcular el tiempo transcurrido  
    print(f"Bienvenido sr. {usuario.name} Tiempo transcurrido: {elapsed_time} segundos")
            
