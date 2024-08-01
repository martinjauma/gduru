import streamlit as st
import json
import uuid
import requests
from datetime import datetime
import base64

# Intentar acceder al secreto GITHUB_TOKEN
try:
    GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
    st.write("GITHUB_TOKEN encontrado en secretos.")
except KeyError:
    st.error("GITHUB_TOKEN no encontrado en secretos. Asegúrate de que está configurado correctamente.")
    st.stop()

REPO_OWNER = "martinjauma"
REPO_NAME = "gduru"
FILE_PATH = "json/datos.json"

def leer_datos():
    # Agregar un indicador de carga
    with st.spinner('Cargando datos...'):
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3.raw"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return json.loads(response.content)
        return []

def escribir_datos(datos):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    if response.status_code == 200:
            sha = response.json()["sha"]
    else:
            sha = None
    contenido_encoded = base64.b64encode(json.dumps(datos).encode()).decode()
    data = {
            "message": "Actualizar datos.json",
            "content": contenido_encoded,
            "branch": "main"
    }
    if sha:
            data["sha"] = sha
    response = requests.put(url, headers=headers, data=json.dumps(data))
    return response.status_code == 200 or response.status_code == 201

st.title("Formulario de Datos")

def mostrar_registros(datos):
    st.subheader("Registros")
    for registro in datos:
        st.write(registro)

# Cargar los datos iniciales
datos = leer_datos()

with st.form("Agregar Registro"):
    nombre = st.text_input("Nombre")
    edad = st.number_input("Edad", min_value=0, max_value=120)
    altura = st.number_input("Altura (cm)", min_value=0)
    peso = st.number_input("Peso (kg)", min_value=0)
    submitted = st.form_submit_button("Agregar")

    if submitted:
        nuevo_registro = {
            "id": str(uuid.uuid4()),
            "nombre": nombre,
            "edad": edad,
            "altura": altura,
            "peso": peso,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        datos.append(nuevo_registro)
        if escribir_datos(datos):
            # Actualizar la lista local directamente y mostrar mensaje de éxito
            datos = leer_datos()  # Recargar los datos para asegurar la consistencia
            mostrar_registros(datos)
            st.success("Registro agregado exitosamente.")
        else:
            st.error("Hubo un problema al agregar el registro.")


# Mostrar los registros iniciales
mostrar_registros(datos)
