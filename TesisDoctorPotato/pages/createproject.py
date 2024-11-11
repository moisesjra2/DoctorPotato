import streamlit as st
import login
import mysql.connector
import time
import torch  # Para cargar el modelo YOLOv10
import cv2  # Para procesar imágenes y videos
import tempfile
from PIL import Image
import numpy as np
import os
import io
from ultralytics import YOLOv10
from mysql.connector import Error
from datetime import datetime

#st.session_state.video_data = None  # Liberar el video procesado después de descargar
#st.session_state.video_path = None  # También liberar el path del video original si es necesario
#st.session_state.processed_image_data = None
#st.session_state.uploaded_image = None

# Función para obtener usuarios con roles específicos
def get_users_by_role(role_list):
    try:
        connection = mysql.connector.connect(
            host='34.31.255.172',  # Cambia esto por tu host de base de datos
            user="root",       # Tu usuario de MySQL
            password='2572691Aa#',  # Tu contraseña de MySQL
            database='db_seguridadbuilding'  # Nombre de tu base de datos
        )
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            query = "SELECT UsuarioId, UsuarioUserName FROM Usuario WHERE UsuarioRoleName IN (%s)" % ','.join(['%s']*len(role_list))
            cursor.execute(query, tuple(role_list))
            users = cursor.fetchall()
            return users
    except Error as e:
        st.error(f"Error al conectar con la base de datos: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Función para insertar un nuevo proyecto en la base de datos
def insert_project(proyecto_name, proyecto_date, imagen_procesada, video_procesado, responsable_id, usuario_id):
    try:
        connection = mysql.connector.connect(
            host='34.31.255.172',  # Cambia esto por tu host de base de datos
            user="root",       # Tu usuario de MySQL
            password='2572691Aa#',  # Tu contraseña de MySQL
            database='db_seguridadbuilding'  # Nombre de tu base de datos
        )
        if connection.is_connected():
            cursor = connection.cursor()
            query = """INSERT INTO Proyecto
                       (ProyectoName, ProyectoDate, ProyectoImagenProcesada, ProyectoVideoProcesado, ResponsableId, UsuarioId)
                       VALUES (%s, %s, %s, %s, %s, %s)"""
            values = (proyecto_name, proyecto_date, imagen_procesada, video_procesado, responsable_id, usuario_id)
            cursor.execute(query, values)
            connection.commit()
            st.success("¡Proyecto creado exitosamente!")
    except Error as e:
        st.error(f"Error al conectar con la base de datos: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def img_changed():
    st.session_state['ImgChanged'] = True

def vid_changed():
    st.session_state['VidChanged'] = True

login.generarLogin()
if 'usuario' in st.session_state:
    
    st.header(':blue[Crear Proyecto]')


    # Obtener usuarios para combos
    responsables = get_users_by_role(['admin', 'operador'])
    usuarios = get_users_by_role(['agricultor'])


    proyecto_name = st.text_input("Nombre del proyecto")
    proyecto_date = st.date_input("Fecha", min_value=datetime.today())

    responsable_id = st.selectbox(
        "Responsable",
        options=[user['UsuarioId'] for user in responsables],
        format_func=lambda x: next(user['UsuarioUserName'] for user in responsables if user['UsuarioId'] == x)
    )
    
    usuario_id = st.selectbox(
        "Agricultor",
        options=[user['UsuarioId'] for user in usuarios],
        format_func=lambda x: next(user['UsuarioUserName'] for user in usuarios if user['UsuarioId'] == x)
    )

    
    model = YOLOv10(f'best.pt')
    

        # Al principio del archivo, asegúrate de inicializar st.session_state para la imagen procesada
    if 'processed_image_data' not in st.session_state:
        st.session_state.processed_image_data = None  # Inicializa como None si no existe

    if 'uploaded_image' not in st.session_state:
        st.session_state.uploaded_image = None  # Inicializa la imagen original como None

    #st.session_state['ImgChanged'] = False
    imagen_sin_procesar = st.file_uploader("Subir imagen a procesar", type=["jpg", "jpeg", "png"], on_change = img_changed)

    if imagen_sin_procesar and st.session_state['ImgChanged'] :
        
        st.session_state.processed_image_data = None
        # Cargar la imagen
        image = Image.open(imagen_sin_procesar)
        st.session_state.uploaded_image = image  # Guardar la imagen original en la sesión

        # Procesar la imagen con el modelo YOLOv10
        results = model(image, conf=0.25, save=False)
        
        # Obtener la imagen procesada en un array de numpy
        processed_image = results[0].plot()

        # Convertir el array de numpy a imagen PIL
        processed_image_pil = Image.fromarray(cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB))

        # Guardar la imagen procesada en un archivo temporal para la descarga
        buffered = io.BytesIO()
        processed_image_pil.save(buffered, format="PNG")
        st.session_state.processed_image_data = buffered.getvalue()  # Guardar la imagen procesada en la sesión

        st.session_state['ImgChanged'] = False

        

    # Mostrar la imagen original y procesada si ya existe en session_state
    if st.session_state.processed_image_data:
        
        col1, col2 = st.columns(2)

        # Mostrar la imagen subida en la primera columna
        with col1:
            st.header("Imagen Subida")
            st.image(st.session_state.uploaded_image, caption="Imagen Subida", use_column_width=True)

        # Mostrar la imagen procesada en la segunda columna
        with col2:
            st.header("Imagen Procesada")
            st.image(st.session_state.processed_image_data, caption="Imagen Procesada", use_column_width=True)

        #col1, col2, col3 = st.columns(3)
        #****************









    # Al principio del archivo, asegúrate de inicializar st.session_state para el video procesado
    if 'video_data' not in st.session_state:
        st.session_state.video_data = None  # Inicializa la clave como None si no existe

    if 'video_path' not in st.session_state:
        st.session_state.video_path = None  # Inicializa el path del video original
 

    video_sin_procesado = st.file_uploader("Subir video a procesar", type=["mp4", "avi", "mov"], on_change = vid_changed)


    if video_sin_procesado and st.session_state['VidChanged']:

        st.session_state.video_data = None
        # Guardar el archivo de video temporalmente
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        tfile.write(video_sin_procesado.read())
        video_path = tfile.name
        st.session_state.video_path = video_path  # Guarda el path del video original

        # Procesar el video con YOLOv10 y guardar los frames en memoria
        results = model(source=video_path, conf=0.25, save=False)

        # Crear una lista para guardar los frames procesados
        processed_frames = []

        # Recorrer los resultados y obtener frames procesados
        for result in results:
            frame = result.plot()  # Obtener el frame procesado como un array de numpy
            processed_frames.append(frame)

        # Crear un video a partir de los frames procesados
        frame_height, frame_width = processed_frames[0].shape[:2]
        video_output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        video_output_path.close()  # Cerrar el archivo para permitir que se escriba más tarde

        # Guardar los frames en un nuevo archivo de video
        out = cv2.VideoWriter(video_output_path.name, cv2.VideoWriter_fourcc(*'mp4v'), 30, (frame_width, frame_height))

        for frame in processed_frames:
            out.write(frame)
        out.release()

        # Leer el video procesado en memoria
        with open(video_output_path.name, "rb") as video_file:
            st.session_state.video_data = video_file.read()  # Guarda el video procesado en la sesión
    
        st.session_state['VidChanged'] = False


    # Mostrar el video procesado y original si ya existe en session_state
    if st.session_state.video_data:
        col1, col2, col3 = st.columns(3)
        with col2:
            st.header("Video Original")
            st.video(st.session_state.video_path)  # Muestra el video original desde el path
            
            # Ofrecer el video procesado para descarga
            #*********

    #st.session_state['ImgChanged'] = False
    #st.session_state['VidChanged'] = False
    submit = st.button("Crear Proyecto")
    
    if submit:
        if imagen_sin_procesar and video_sin_procesado:
        
            # Llamar a la función para insertar el proyecto en la base de datos
            insert_project(
                proyecto_name,
                proyecto_date,
                st.session_state.processed_image_data,
                st.session_state.video_data,
                responsable_id,
                usuario_id
            )

            st.session_state.processed_image_data = None
            st.session_state.uploaded_image = None

            st.session_state.video_data = None 
            st.session_state.video_path = None

            st.switch_page("pages/listproject.py")


        else:
            st.error("Por favor, sube ambos archivos de imagen y video.")
