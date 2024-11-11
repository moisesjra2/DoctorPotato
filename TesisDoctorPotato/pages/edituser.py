import streamlit as st
import login
import mysql.connector
import time
from mysql.connector import Error


# Función para verificar si el usuario ya existe en la base de datos
def verificar_usuario_existente(username):
    try:
        connection = mysql.connector.connect(
            host='34.31.255.172',  
            user="root",       
            password='2572691Aa#',  
            database='db_seguridadbuilding'  
        )
        if connection.is_connected():
            cursor = connection.cursor()
            query = "SELECT COUNT(*) FROM Usuario WHERE UsuarioUserName = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            return result[0] > 0  # Retorna True si el usuario ya existe
    
    except Error as e:
        st.error(f"Error al conectar con la base de datos: {e}")
        return False
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# Función para obtener los datos del usuario
def get_user(userid):
    try:
        connection = mysql.connector.connect(
            host='34.31.255.172',  # Cambia esto por tu host de base de datos
            user="root",       # Tu usuario de MySQL
            password='2572691Aa#',  # Tu contraseña de MySQL
            database='db_seguridadbuilding'  # Nombre de tu base de datos
        )
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM Usuario WHERE UsuarioId = %s"
            cursor.execute(query, (userid,))
            user = cursor.fetchone()
            return user
    except Error as e:
        st.error(f"Error al conectar con la base de datos: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Función para actualizar los datos del usuario
def update_user(user_id, username, clave, nombres, apellidos, role_name):
    try:
        connection = mysql.connector.connect(
            host='34.31.255.172',  # Cambia esto por tu host de base de datos
            user="root",       # Tu usuario de MySQL
            password='2572691Aa#',  # Tu contraseña de MySQL
            database='db_seguridadbuilding'  # Nombre de tu base de datos
        )
        if connection.is_connected():
            cursor = connection.cursor()
            query = """UPDATE Usuario
                       SET UsuarioUserName = %s, UsuarioClave = %s, UsuarioNombres = %s, UsuarioApellidos = %s, UsuarioRoleName = %s
                       WHERE UsuarioId= %s"""
            values = (username, clave, nombres, apellidos, role_name, user_id)
            cursor.execute(query, values)
            connection.commit()
            if cursor.rowcount > 0:
                st.success("¡Usuario actualizado exitosamente!")
            else:
                st.warning("No se encontró ningún usuario con ese nombre.")
    except Error as e:
        st.error(f"Error al conectar con la base de datos: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


login.generarLogin()
if 'usuario' in st.session_state:
    st.header(':blue[Editar usuario]')

    user = get_user(st.session_state['edituserid'])

    if user:
        with st.form("Formulario Editar Usuario"):
            user_id = st.text_input("ID", value=user['UsuarioId'], disabled=True)
            username = st.text_input("UserName", value=user['UsuarioUserName'])
            clave = st.text_input("Clave", type="password", value=user['UsuarioClave'])
            nombres = st.text_input("Nombres", value=user['UsuarioNombres'])
            apellidos = st.text_input("Apellidos", value=user['UsuarioApellidos'])
            role_name = st.selectbox(
                "Role", 
                options=["admin", "operador", "agricultor"],  # Opciones del combo
                index=["admin", "operador", "agricultor"].index(user['UsuarioRoleName'])
            )

            submit = st.form_submit_button("Actualizar Usuario")

            if submit:

                if username == "" or clave == "" or nombres == "" or apellidos == "" or role_name == "":
                    
                    st.error("Complete los campos vacíos")

                else:
                    auxnombres = nombres
                    auxapellidos = apellidos
                    auxnombres = auxnombres.replace(" ", "")
                    auxapellidos = auxapellidos.replace(" ", "")
                    
                    if not auxnombres.isalpha() or not auxapellidos.isalpha():
                        st.error("Los nombres y apellidos deben contener solo letras.")
                    else:    
                        if verificar_usuario_existente(username):
                            st.warning("El usuario ya existe en el sistema.")
                        else:

                            if len(clave) > 0 and len(clave) <5 and clave != "" :
                                st.error("La clave debe ser mayor o igual a 5 caracteres")
                            else:
                                update_user(user_id, username, clave, nombres, apellidos, role_name)
                                time.sleep(2)
                                st.switch_page("pages/listuser.py")
                
    else:
        st.warning("No se encontró ningún usuario con ese nombre.")


