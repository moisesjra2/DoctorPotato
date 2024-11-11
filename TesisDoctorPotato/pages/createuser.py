import streamlit as st
import login
import mysql.connector
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


def insert_user(username, clave, nombres, apellidos, role_name):
    try:
        connection = mysql.connector.connect(
            host='34.31.255.172',  # Cambia esto por tu host de base de datos
            user="root",       # Tu usuario de MySQL
            password='2572691Aa#',  # Tu contraseña de MySQL
            database='db_seguridadbuilding'  # Nombre de tu base de datos
        )
        if connection.is_connected():
            cursor = connection.cursor()
            query = """INSERT INTO Usuario 
                       (UsuarioUserName, UsuarioClave, UsuarioNombres, UsuarioApellidos, UsuarioRoleName) 
                       VALUES (%s, %s, %s, %s, %s)"""
            values = (username, clave, nombres, apellidos, role_name)
            cursor.execute(query, values)
            connection.commit()
            st.success("¡Usuario creado exitosamente!")
    
    except Error as e:
        st.error(f"Error al conectar con la base de datos: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


login.generarLogin()
if 'usuario' in st.session_state:
    st.header(':blue[Crear usuario]')

    with st.form("Formulario Crear Usuario"):
        username = st.text_input("Usuario")
        clave = st.text_input("Clave", type="password")
        nombres = st.text_input("Nombres")
        apellidos = st.text_input("Apellidos")
         
        # Campo selectbox para Role Name
        role_name = st.selectbox(
            "Role", 
            options=["admin", "operador", "agricultor"]  # Opciones del combo
        )

        submit = st.form_submit_button("Crear Usuario")

        if submit:
           if username == "" or clave == "" or nombres == "" or apellidos == "":

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
                            insert_user(username, clave, nombres, apellidos, role_name)
                            st.switch_page("pages/listuser.py")   
