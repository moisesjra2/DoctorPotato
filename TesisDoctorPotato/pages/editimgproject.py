import streamlit as st
import login
import mysql.connector
import time
import cv2  # Para procesar imágenes y videos
import tempfile
from PIL import Image
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

def get_project(projectid):
    try:
        connection = mysql.connector.connect(
            host='34.31.255.172',  # Cambia esto por tu host de base de datos
            user="root",       # Tu usuario de MySQL
            password='2572691Aa#',  # Tu contraseña de MySQL
            database='db_seguridadbuilding'  # Nombre de tu base de datos
        )
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM Proyecto WHERE ProyectoId = %s"
            cursor.execute(query, (projectid,))
            project = cursor.fetchone()
            return project
    except Error as e:
        st.error(f"Error al conectar con la base de datos: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def update_project(projectid, projectimg):
    try:
        connection = mysql.connector.connect(
            host='34.31.255.172',  # Cambia esto por tu host de base de datos
            user="root",       # Tu usuario de MySQL
            password='2572691Aa#',  # Tu contraseña de MySQL
            database='db_seguridadbuilding'  # Nombre de tu base de datos
        )
        if connection.is_connected():
            cursor = connection.cursor()
            query = """UPDATE Proyecto
                       SET ProyectoImagenProcesada = %s
                       WHERE ProyectoId= %s"""
            values = (projectimg, projectid)
            cursor.execute(query, values)
            connection.commit()
            st.success("¡Proyecto actualizado exitosamente!")

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
    
    st.header(":blue[Agregar Imagen al proyecto]")

    project = get_project(st.session_state['editprojectid'])

    if project:

        proyecto_id = st.text_input("ID", value=project['ProyectoId'], disabled=True)
        proyecto_name = st.text_input("Nombre del proyecto", value=project['ProyectoName'], disabled=True)
        
        model = YOLOv10(f'best.pt')
        

            # Al principio del archivo, asegúrate de inicializar st.session_state para la imagen procesada
        if 'processed_image_data' not in st.session_state:
            st.session_state.processed_image_data = None  # Inicializa como None si no existe

        if 'uploaded_image' not in st.session_state:
            st.session_state.uploaded_image = None  # Inicializa la imagen original como None

        imagen_sin_procesar = st.file_uploader("Subir imagen a procesar", type=["jpg", "jpeg", "png"])

        if imagen_sin_procesar:
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



        submit = st.button(":material/update: Actualizar Proyecto")
        
        if submit:
            
            # Llamar a la función para insertar el proyecto en la base de datos
            update_project(
                proyecto_id,
                st.session_state.processed_image_data,
            )

            st.session_state.processed_image_data = None
            st.session_state.uploaded_image = None

            st.switch_page("pages/listproject.py")


    else:
        st.warning("No se encontró ningún proyecto.")

      

    
