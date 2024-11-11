import streamlit as st
import login
import mysql.connector
from mysql.connector import Error
import pandas as pd


def delete_user(username):
    try:
        connection = mysql.connector.connect(
            host='34.31.255.172',  # Cambia esto por tu host de base de datos
            user="root",       # Tu usuario de MySQL
            password='2572691Aa#',  # Tu contraseña de MySQL
            database='db_seguridadbuilding'  # Nombre de tu base de datos
        )
        if connection.is_connected():
            cursor = connection.cursor()
            query = "DELETE FROM Usuario WHERE UsuarioUserName = %s"
            values = (username,)
            cursor.execute(query, values)
            connection.commit()
            st.success("¡Usuario eliminado exitosamente!")
    
    except Error as e:
        st.error(f"Error al conectar con la base de datos: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()




db_user = 'root'
db_password = '2572691Aa#'
db_host = '34.31.255.172'  # Usualmente es la dirección IP de tu servidor GCP
db_name = 'db_seguridadbuilding'


# Crear la conexión a la base de datos
def create_connection():
    return mysql.connector.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        database=db_name
    )

# Función para obtener todos los datos de una tabla
def obtener_datos_tabla():
    conn = create_connection()
    query = "SELECT * FROM Usuario Where not UsuarioUserName = %s"  # Reemplaza "NombreDeTuTabla" por el nombre real de tu tabla
    
    #df = pd.read_sql(query, conn)
    df = pd.read_sql(query, conn, params=(st.session_state['usuario'],))
    conn.close()
    return df

def mostrar_usuarios_con_boton(datos_usuarios):
    col1, col2, col3, col4, col5, col6 = st.columns([2, 3, 3, 3, 2, 3])  # Dividimos en columnas
    col1.write('Id')  # Columna de ID
    col2.write('UserName')  # Columna de Nombre de Usuario
    col3.write('Nombres')  # Columna de Nombre Completo
    col4.write('RoleName')  # Columna de Rol
    col5.write('Accion')
    col6.write('Accion')
    for index, row in datos_usuarios.iterrows():
        
        col1, col2, col3, col4, col5, col6 = st.columns([2, 3, 3, 3, 2, 3])  # Dividimos en columnas
        col1.write(row['UsuarioId'])  # Columna de ID
        col2.write(row['UsuarioUserName'])  # Columna de Nombre de Usuario
        col3.write(row['UsuarioNombres'])  # Columna de Nombre Completo
        col4.write(row['UsuarioRoleName'])  # Columna de Rol

        # Columna de botón de edición
        if col5.button("Editar", type="secondary",key=row['UsuarioId']):
            # Establecer el parámetro en la URL con el id del usuario
            st.session_state['edituserid'] = row['UsuarioId']
            st.switch_page("pages/edituser.py")

        with col6.popover(":material/delete:"):

            st.write("¿Seguro que quieres Eliminar?")

            if st.button("Sí", key=row['UsuarioUserName']):
                delete_user(row['UsuarioUserName'])
                st.rerun()

            
            






login.generarLogin()
if 'usuario' in st.session_state:
    st.header(':blue[Lista de usuarios]')
    st.page_link("pages/createuser.py", label="Nuevo Usuario", icon=":material/add_circle:")
    

    datos = obtener_datos_tabla()
    mostrar_usuarios_con_boton(datos)



