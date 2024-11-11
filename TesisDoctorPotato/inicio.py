import streamlit as st
import login as login


login.generarLogin()
if 'usuario' in st.session_state:

    # Crear columnas para centrar el contenido
    col1, col2, col3 = st.columns([1, 2, 1])  # Las columnas exteriores son más pequeñas para centrar

    with col2:  # Contenido centrado en la columna del medio
        col_left, col_right = st.columns([1, 3], gap='large')  # Imagen y texto juntos

    with col_left:
        st.image("Doctor potato Logo.jpg", width=100)  # Imagen más pequeña para alinearse bien
    with col_right:
        st.header("DOCTOR POTATO")

    # Párrafos
    st.write("""
    Bienvenido al Sistema de Detección de Enfermedades en Cultivos de Papa. 
    Este sistema está diseñado para facilitar el monitoreo y análisis de los cultivos de papa, permitiendo la identificación temprana de enfermedades como el tizón temprano y tardío. 

    Utilizando imágenes capturadas por drones y un modelo avanzado de redes neuronales convolucionales (CNN), nuestro sistema analiza los datos visuales para ayudar a las PYMES agrícolas a optimizar la salud de sus cultivos y mejorar su producción.

    Desde esta plataforma, puedes gestionar usuarios, proyectos y acceder a reportes detallados que apoyarán la toma de decisiones en tus operaciones agrícolas.
    """)