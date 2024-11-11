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




def delete_project(proyectoid):
    try:
        connection = mysql.connector.connect(
            host='34.31.255.172',  # Cambia esto por tu host de base de datos
            user="root",       # Tu usuario de MySQL
            password='2572691Aa#',  # Tu contraseña de MySQL
            database='db_seguridadbuilding'  # Nombre de tu base de datos
        )
        if connection.is_connected():
            cursor = connection.cursor()
            query = "DELETE FROM Proyecto WHERE ProyectoId = %s"
            values = (proyectoid,)
            cursor.execute(query, values)
            connection.commit()
            st.success("¡Proyecto eliminado exitosamente!")
    
    except Error as e:
        st.error(f"Error al conectar con la base de datos: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



def get_projects():
    
    try:
        connection = mysql.connector.connect(
            host='34.31.255.172',  # Cambia esto por tu host de base de datos
            user="root",       # Tu usuario de MySQL
            password='2572691Aa#',  # Tu contraseña de MySQL
            database='db_seguridadbuilding'  # Nombre de tu base de datos
        )
        if connection.is_connected():
            cursor = connection.cursor()
            query = "Select * FROM Proyecto"
            cursor.execute(query)
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
    col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([2, 3, 2, 2, 2, 3, 3, 2, 2])   # Dividimos en columnas
    col1.write('Id')
    col2.write('Nombre')
    col3.write('Fecha')
    col4.write('ImgPro')
    col5.write('VidPro')
    col6.write('Responsable')
    col7.write('Usuario')
    col8.write('Edit')
    col9.write('Delete')

    for index, row in projects.iterrows():
        
        col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([2, 3, 2, 2, 2, 3, 3, 2, 2])  # Dividimos en columnas
        with col1:
            row['ProyectoId']
        with col2:
            row['ProyectoName']
        with col3:
            row['ProyectoDate']
        with col4:
            if row['ProyectoImagenProcesada'] == None:
            
                if st.button(":material/edit:", type="secondary", key=f"edit_img_{row['ProyectoName']}"):
                    # Establecer el parámetro en la URL con el id del usuario
                    st.session_state['editprojectid'] = row['ProyectoId']
                    st.switch_page("pages/editimgproject.py")

            else:
                st.download_button(
                label=":material/image:",
                data=row['ProyectoImagenProcesada'],
                file_name=  "ImagenProcesada_"+ row['ProyectoName'] + ".png",
                mime="image/png"
            )
                 
            
        with col5:

            if row['ProyectoVideoProcesado'] == None:
                if st.button(":material/edit:", type="secondary", key=f"edit_vid_{row['ProyectoName']}"):
                    # Establecer el parámetro en la URL con el id del usuario
                    st.session_state['editprojectid'] = row['ProyectoId']
                    st.switch_page("pages/editvideoproject.py")


            else:

                st.download_button(
                    label=":material/smart_display:",
                    data=row['ProyectoVideoProcesado'],
                    file_name=  "VideoProcesado_"+ row['ProyectoName'] + ".mp4",
                    mime="video/mp4"
                )
        
        with col6:
            #VALRES = get_user_fullname(row['ResponsableId'])
            #VALRES
            row['ResponsableId']
        with col7:
            row['UsuarioId']

        if col8.button(":material/edit:", type="secondary",key=row['ProyectoId']):
            # Establecer el parámetro en la URL con el id del usuario
            st.session_state['editprojectid'] = row['ProyectoId']
            st.switch_page("pages/editproject.py")

        with col9.popover(":material/delete:"):
            
            st.write("¿Seguro que quieres Eliminar?")
        
            if st.button("Sí", key=row['ProyectoName']):
                delete_project(row['ProyectoId'])
                st.rerun()

                      

login.generarLogin()
if 'usuario' in st.session_state:
    st.header(':blue[Lista de proyectos]')
    st.page_link("pages/createproject.py", label="Nuevo Proyecto", icon=":material/add_circle:")
    

    datos = get_projects()
    List_projects(datos)



