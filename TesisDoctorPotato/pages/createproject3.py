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
def insert_project(proyecto_name, proyecto_date, responsable_id, usuario_id):
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
                       (ProyectoName, ProyectoDate, ResponsableId, UsuarioId)
                       VALUES (%s, %s, %s, %s)"""
            values = (proyecto_name, proyecto_date, responsable_id, usuario_id)
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
    usuarios = get_users_by_role(['usuario'])


    proyecto_name = st.text_input("Nombre del proyecto")
    proyecto_date = st.date_input("Fecha", min_value=datetime.today())

    responsable_id = st.selectbox(
        "Responsable",
        options=[user['UsuarioId'] for user in responsables],
        format_func=lambda x: next(user['UsuarioUserName'] for user in responsables if user['UsuarioId'] == x)
    )
    
    usuario_id = st.selectbox(
        "Usuario",
        options=[user['UsuarioId'] for user in usuarios],
        format_func=lambda x: next(user['UsuarioUserName'] for user in usuarios if user['UsuarioId'] == x)
    )

    
   
    submit = st.button("Crear Proyecto")
    
    if submit:
        if not proyecto_name == "":
        
            # Llamar a la función para insertar el proyecto en la base de datos
            insert_project(
                proyecto_name,
                proyecto_date,
                responsable_id,
                usuario_id
            )

            st.session_state.processed_image_data = None
            st.session_state.uploaded_image = None

            st.session_state.video_data = None 
            st.session_state.video_path = None

            st.switch_page("pages/listproject.py")


        else:
            st.error("Por favor, ingrese un nombre al proyecto.")
