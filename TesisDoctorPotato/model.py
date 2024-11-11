import streamlit as st
#import torch  # Para cargar el modelo YOLOv10
import cv2  # Para procesar imágenes y videos
import tempfile
from PIL import Image
import numpy as np
import os
import io
from ultralytics import YOLOv10

model = YOLOv10(f'best.pt')

# Título de la aplicación
st.title("Detección de Enfermedades en Hojas de Papa")

# Menú de opciones: Imagen o Video
option = st.selectbox("Selecciona el tipo de archivo", ("Imagen", "Video"))

# Subida de archivo
uploaded_file = st.file_uploader("Sube una imagen o video", type=["jpg", "jpeg", "png", "mp4"])

# Procesar Imagen
if uploaded_file and option == "Imagen":
   
    image = Image.open(uploaded_file)
    results = model(image, conf=0.25,save=False)

    # Obtener la imagen procesada en memoria
    processed_image = results[0].plot()  # Obtener la imagen procesada como un array de numpy

    # Convertir el array a una imagen PIL
    processed_image_pil = Image.fromarray(cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB))


    col1, col2 = st.columns(2)

    # Mostrar la imagen subida en la primera columna
    with col1:
        st.header("Imagen Subida")
        st.image(uploaded_file, caption="Imagen Subida", use_column_width=True)

    # Mostrar la imagen procesada en la segunda columna
    with col2:
        st.header("Imagen Procesada")
        st.image(processed_image_pil, caption="Imagen Procesada", use_column_width=True)


     # Guardar la imagen procesada en un archivo temporal para la descarga
    buffered = io.BytesIO()
    processed_image_pil.save(buffered, format="PNG")
    st.download_button(
        label="Descargar Imagen Procesada",
        data=buffered.getvalue(),
        file_name="imagen_procesada.png",
        mime="image/png"
    )


# Procesar Video
elif uploaded_file and option == "Video":
    
     
    # Guardar el archivo de video temporalmente
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(uploaded_file.read())
    video_path = tfile.name

    # Crear un archivo temporal para el video procesado
    temp_processed_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_processed_video.close()  # Cerrar el archivo para permitir que se escriba más tarde

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
        video_data = video_file.read()

    # Mostrar el video original y el procesado en columnas
    col1, col2 = st.columns(2)
    with col1:
        st.header("Video Original")
        st.video(video_path)

    with col2:
        st.header("Video Procesado")
        st.video(io.BytesIO(video_data))  # Mostrar el video procesado desde memoria

    # Ofrecer el video procesado para descarga
    st.download_button(
        label="Descargar Video Procesado",
        data=video_data,
        file_name="video_procesado.mp4",
        mime="video/mp4"
    )

