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


def update_project(projectid, projectvid):
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
                       SET ProyectoVideoProcesado = %s
                       WHERE ProyectoId= %s"""
            values = (projectvid, projectid)
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
    
    st.header(":blue[Agregar Video al proyecto]")

    project = get_project(st.session_state['editprojectid'])

    def vid_changed():
        st.session_state['VidChanged'] = True

    if project:

        proyecto_id = st.text_input("ID", value=project['ProyectoId'], disabled=True)
        proyecto_name = st.text_input("Nombre del proyecto", value=project['ProyectoName'], disabled=True)
        
        model = YOLOv10(f'best.pt')
        
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

        # Mostrar el video procesado y original si ya existe en session_state
        if st.session_state.video_data:
            col1, col2, col3 = st.columns(3)
            with col2:
                st.header("Video Original")
                st.video(st.session_state.video_path)  # Muestra el video original desde el path
                
        st.session_state['VidChanged'] = False
        submit = st.button(":material/update: Actualizar Proyecto")
        
        if submit:
            if video_sin_procesado:
            
                # Llamar a la función para insertar el proyecto en la base de datos
                update_project(
                    proyecto_id,
                    st.session_state.video_data,
                )

                st.session_state.processed_image_data = None
                st.session_state.uploaded_image = None

                st.session_state.video_data = None 
                st.session_state.video_path = None

                st.switch_page("pages/listproject.py")


            else:
                st.warning("No se encontró ningún proyecto.")

      

    
