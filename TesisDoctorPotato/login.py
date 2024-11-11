import streamlit as st
import mysql.connector
from mysql.connector import Error


def validarUsuario(usuario,clave):    
    
    try:
        connection = mysql.connector.connect(
            host='34.31.255.172',  # Cambia esto por tu host de base de datos
            user="root",       # Tu usuario de MySQL
            password='2572691Aa#',  # Tu contraseña de MySQL
            database='db_seguridadbuilding'  # Nombre de tu base de datos
        )
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM Usuario WHERE UsuarioUserName = %s AND UsuarioClave = %s"
            cursor.execute(query, (usuario, clave))
            result = cursor.fetchone()
            if result:
                return True
            else:
                return False
            
    except Error as e:
        st.error(f"Error al conectar con la base de datos: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



def obtenerUsuarioRole(usuario,clave):    
       
    try:
        connection = mysql.connector.connect(
            host='34.31.255.172',  # Cambia esto por tu host de base de datos
            user="root",       # Tu usuario de MySQL
            password='2572691Aa#',  # Tu contraseña de MySQL
            database='db_seguridadbuilding'  # Nombre de tu base de datos
        )
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            query = "SELECT UsuarioNombres, UsuarioRoleName FROM Usuario WHERE UsuarioUserName = %s AND UsuarioClave = %s"
            cursor.execute(query, (usuario, clave))
            result = cursor.fetchone()
            
            if result:
                return result['UsuarioNombres'], result['UsuarioRoleName']
            else:
                return None
            
    except Error as e:
        st.error(f"Error al conectar con la base de datos: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()    
    


def obtenerRolexUsuario(usuario):    

    try:
        connection = mysql.connector.connect(
            host='34.31.255.172',  # Cambia esto por tu host de base de datos
            user="root",       # Tu usuario de MySQL
            password='2572691Aa#',  # Tu contraseña de MySQL
            database='db_seguridadbuilding'  # Nombre de tu base de datos
        )
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            query = "SELECT UsuarioRoleName FROM Usuario WHERE UsuarioUserName = %s"
            cursor.execute(query, (usuario,))
            result = cursor.fetchone()
            
            if result:
                return result['UsuarioRoleName']
            else:
                return None
            
    except Error as e:
        st.error(f"Error al conectar con la base de datos: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()    



def obtenerUsuarioId(usuario):    
    
    try:
        connection = mysql.connector.connect(
            host='34.31.255.172',  # Cambia esto por tu host de base de datos
            user="root",       # Tu usuario de MySQL
            password='2572691Aa#',  # Tu contraseña de MySQL
            database='db_seguridadbuilding'  # Nombre de tu base de datos
        )
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            query = "SELECT UsuarioId FROM Usuario WHERE UsuarioUserName = %s"
            cursor.execute(query, (usuario,))
            result = cursor.fetchone()
            
            if result:
                return result['UsuarioId']
            else:
                return None
            
    except Error as e:
        st.error(f"Error al conectar con la base de datos: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close() 


def obtenerUsuarioNombres(usuario):    
    
    try:
        connection = mysql.connector.connect(
            host='34.31.255.172',  # Cambia esto por tu host de base de datos
            user="root",       # Tu usuario de MySQL
            password='2572691Aa#',  # Tu contraseña de MySQL
            database='db_seguridadbuilding'  # Nombre de tu base de datos
        )
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            query = "SELECT UsuarioNombres FROM Usuario WHERE UsuarioUserName = %s"
            cursor.execute(query, (usuario,))
            result = cursor.fetchone()
            
            if result:
                return result['UsuarioNombres']
            else:
                return None
            
    except Error as e:
        st.error(f"Error al conectar con la base de datos: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()     



def generarMenu(): 
        
    with st.sidebar:
        
        st.write('Role: ' + st.session_state['userrole'])
        #Mostramos el nombre del usuario
        st.write(f"Hola **:blue-background[{st.session_state['userfirstname']}]** ")
        


        if st.session_state['userrole'] == "admin":

            # Mostramos los enlaces de páginas
            st.page_link("inicio.py", label="Inicio", icon=":material/home:")
            
            st.subheader("Usuarios")
            st.page_link("pages/listuser.py", label="Listar Usuarios", icon=":material/patient_list:")
            st.page_link("pages/createuser.py", label="Crear Usuario", icon=":material/person_add:")

            st.subheader("Proyectos")
            st.page_link("pages/listproject.py", label="Listar Proyectos", icon=":material/patient_list:")
            st.page_link("pages/createproject.py", label="Crear Proyecto", icon=":material/create_new_folder:")
        
        

        if st.session_state['userrole'] == "operador":

            # Mostramos los enlaces de páginas
            st.page_link("inicio.py", label="Inicio", icon=":material/home:")
        
            st.subheader("Proyectos")
            st.page_link("pages/listproject.py", label="Listar Proyectos", icon=":material/patient_list:")
            st.page_link("pages/createproject.py", label="Crear Proyecto", icon=":material/create_new_folder:")
        


        if st.session_state['userrole'] == "agricultor":

            # Mostramos los enlaces de páginas
            st.page_link("inicio.py", label="Inicio", icon=":material/home:")
            
            st.subheader("Mis Proyectos")
            st.page_link("pages/listproject agricultor.py", label="Listar Proyectos", icon=":material/patient_list:")
            



        st.subheader("Cerrar Sesion")
        # Botón para cerrar la sesión
        btnSalir=st.button("Salir")
        if btnSalir:
            st.session_state.clear()
            # Luego de borrar el Session State reiniciamos la app para mostrar la opción de usuario y clave
            st.rerun()



def generarLogin():
    """Genera la ventana de login o muestra el menú si el login es valido
    """    
    # Validamos si el usuario ya fue ingresado    
    if 'usuario' in st.session_state:
        generarMenu() # Si ya hay usuario cargamos el menu        
    else: 
        st.header('Iniciar Sesión')
        # Cargamos el formulario de login       
        with st.form('frmLogin'):
            parUsuario = st.text_input('Usuario')
            parPassword = st.text_input('Contraseña',type='password')
            btnLogin=st.form_submit_button('Ingresar',type='primary')
            if btnLogin:
                if validarUsuario(parUsuario,parPassword):
                    st.session_state['usuario'] = parUsuario
                    st.session_state['userid'] = obtenerUsuarioId(parUsuario)
                    st.session_state['userfirstname'] = obtenerUsuarioNombres(parUsuario)
                    st.session_state['userrole'] = obtenerRolexUsuario(parUsuario)

                    # Si el usuario es correcto reiniciamos la app para que se cargue el menú
                    st.switch_page("inicio.py")
                    st.rerun()

                else:
                    # Si el usuario es invalido, mostramos el mensaje de error
                    st.error("Usuario o clave inválidos",icon=":material/gpp_maybe:") 