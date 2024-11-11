import streamlit as st
import login
import mysql.connector
from mysql.connector import Error
import pandas as pd
import io


def get_user_fullname(userid):
    try:
        connection = mysql.connector.connect(
            host='34.31.255.172',  # Cambia esto por tu host de base de datos
            user="root",       # Tu usuario de MySQL
            password='2572691Aa#',  # Tu contraseña de MySQL
            database='db_seguridadbuilding'  # Nombre de tu base de datos
        )
        if connection.is_connected():
            cursor = connection.cursor()
            query = "SELECT UsuarioNombres, UsuarioApellidos FROM Usuario WHERE UsuarioId = %s"
            values = (userid,)
            cursor.execute(query, values)
            result = cursor.fetchone

            if result:  # Si se encontró el usuario
                nombre_completo = f"{result[0]} {result[1]}"  # Concatenar nombres y apellidos
                return nombre_completo
            else:
                return None  # Si no se encuentra el usuario, devolver None

    except Error as e:
        st.error(f"Error al conectar con la base de datos: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



def get_total_projectsbyfarmer(userid):

    try:
        connection = mysql.connector.connect(
            host='34.31.255.172',  # Cambia esto por tu host de base de datos
            user="root",       # Tu usuario de MySQL
            password='2572691Aa#',  # Tu contraseña de MySQL
            database='db_seguridadbuilding'  # Nombre de tu base de datos
        )
        if connection.is_connected():
            cursor = connection.cursor()
            query = "SELECT COUNT(*) FROM Proyecto WHERE UsuarioId = %s"
            values = (userid,)
            cursor.execute(query, values)
            result = cursor.fetchone()

            return result[0] if result else 0
        

    except Error as e:
        st.error(f"Error al conectar con la base de datos: {e}")
        return []

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def get_projectsbyfarmer(userid):
    
    try:
        connection = mysql.connector.connect(
            host='34.31.255.172',  # Cambia esto por tu host de base de datos
            user="root",       # Tu usuario de MySQL
            password='2572691Aa#',  # Tu contraseña de MySQL
            database='db_seguridadbuilding'  # Nombre de tu base de datos
        )
        if connection.is_connected():
            cursor = connection.cursor()
            query = "Select * FROM Proyecto WHERE UsuarioId = %s"
            values = (userid,)
            cursor.execute(query, values)
            projects = cursor.fetchall()  # Obtener los resultados de la consulta

            # Obtener los nombres de las columnas de la tabla
            column_names = [i[0] for i in cursor.description]

            # Convertir los resultados a un DataFrame de Pandas
            df_projects = pd.DataFrame(projects, columns=column_names)
            
            #st.success("¡Proyectos listados exitosamente!")
            return df_projects  # Devolver el DataFrame de proyectos
            
    
    except Error as e:
        st.error(f"Error al conectar con la base de datos: {e}")
        return []

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    


def List_projects(projects):
    col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([1, 3, 3, 2, 2, 3, 3, 2, 2])   # Dividimos en columnas
    col1.write('Id')
    col2.write('Nombre')
    col3.write('Fecha')
    col4.write('Imagen')
    col5.write('Video')
    col6.write('Responsable')
    col7.write('Usuario')

    for index, row in projects.iterrows():
        
        col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([1, 3, 3, 2, 2, 3, 3, 2, 2])  # Dividimos en columnas
        with col1:
            row['ProyectoId']
        with col2:
            row['ProyectoName']
        with col3:
            row['ProyectoDate']
        with col4:
            st.download_button(
                label=":material/image:",
                data=row['ProyectoImagenProcesada'],
                file_name=  "ImagenProcesada_"+ row['ProyectoName'] + ".png",
                mime="image/png"
            )
        with col5:
            st.download_button(
                label=":material/smart_display:",
                data=row['ProyectoVideoProcesado'],
                file_name=  "VideoProcesado_"+ row['ProyectoName'] + ".mp4",
                mime="video/mp4"
            )
        
        with col6:
            row['ResponsableId']
        with col7:
            row['UsuarioId']


                      

login.generarLogin()
if 'usuario' in st.session_state:
    st.header(':blue[Lista de proyectos]')
    #st.page_link("pages/createproject.py", label="Nuevo Proyecto", icon=":material/add_circle:")

    if get_total_projectsbyfarmer(st.session_state['userid']) == 0:

        st.warning("Aún no tienes proyectos asignados!")

    else :

        datos = get_projectsbyfarmer(st.session_state['userid'])
        List_projects(datos)



