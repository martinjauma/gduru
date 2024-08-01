import streamlit as st
import json
import os
import uuid
import requests
from datetime import datetime
import base64

# Configura tu token de acceso personal de GitHub y la información del repositorio
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
REPO_OWNER = "martinjauma"
REPO_NAME = "gduru"
FILE_PATH = "json/datos.json"

# Función para generar un ID único para cada registro
def generar_id():
    return str(uuid.uuid4())

# Función para cargar los datos desde el archivo JSON en GitHub
def cargar_datos():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        file_content = response.json()
        return json.loads(base64.b64decode(file_content['content']).decode('utf-8'))
    else:
        return []

# Función para guardar los datos en el archivo JSON en GitHub
def guardar_datos(datos):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    current_data = requests.get(url, headers=headers).json()
    sha = current_data['sha']
    message = "Actualizando datos.json"
    content = json.dumps(datos, indent=4)
    encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    data = {
        "message": message,
        "content": encoded_content,
        "sha": sha
    }
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 201 or response.status_code == 200:
        st.success("Datos guardados exitosamente en GitHub.")
    else:
        st.error(f"Error al guardar los datos en GitHub: {response.json()}")

# Función para eliminar un registro por ID
def eliminar_registro(id_unico):
    datos = cargar_datos()
    registro_eliminado = next((registro for registro in datos if registro["ID"] == id_unico), None)
    datos = [registro for registro in datos if registro["ID"] != id_unico]
    guardar_datos(datos)
    if registro_eliminado:
        st.success(f"Registro: {registro_eliminado['Apellido']}, {registro_eliminado['Nombre']} fue eliminado correctamente.")
    else:
        st.warning(f"No se encontró el registro con ID {id_unico} para eliminar.")

# Función para editar un registro por ID
def editar_registro(id_unico, nuevo_apellido, nuevo_nombre):
    datos = cargar_datos()
    for registro in datos:
        if registro["ID"] == id_unico:
            registro["Apellido"] = nuevo_apellido.capitalize()
            registro["Nombre"] = nuevo_nombre.capitalize()
    guardar_datos(datos)
    st.success(f"Registro: {nuevo_apellido.capitalize()}, {nuevo_nombre.capitalize()} fue editado correctamente.")

# Main Streamlit App ----------------------------------------------

st.title("Formulario de Registro")

# Seleccionar opción
opcion = st.sidebar.selectbox("Seleccione una opción", ["REGISTRAR", "EDITAR", "ELIMINAR"])

if opcion == "REGISTRAR":
    st.subheader("Registrar Nuevo Integrante")

    apellido = st.text_input("Apellido")
    nombre = st.text_input("Nombre")

    if st.button("Registrar"):
        if apellido and nombre:
            datos = cargar_datos()
            nuevo_registro = {
                "ID": generar_id(),
                "Apellido": apellido.capitalize(),
                "Nombre": nombre.capitalize(),
                "Fecha_Registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            datos.append(nuevo_registro)
            guardar_datos(datos)
            st.success(f"{apellido.capitalize()}, {nombre.capitalize()} fue registrado correctamente.")
        else:
            st.warning("Por favor, complete todos los campos.")

elif opcion == "EDITAR":
    st.subheader("Buscar y Editar Registros")

    apellido_buscar = st.text_input("Buscar por Apellido")
    datos = cargar_datos()

    # Filtrar registros por apellido
    registros_filtrados = [registro for registro in datos if apellido_buscar.capitalize() in registro["Apellido"].capitalize()]

    if registros_filtrados:
        apellidos = [registro["Apellido"] for registro in registros_filtrados]
        apellidos_buscar = st.selectbox("Seleccionar Apellido", options=apellidos)

        if apellidos_buscar:
            registro_seleccionado = next((registro for registro in registros_filtrados if registro["Apellido"] == apellidos_buscar), None)
            if registro_seleccionado:
                id_seleccionado = registro_seleccionado["ID"]
                nuevo_apellido = st.text_input("Nuevo Apellido", value=registro_seleccionado["Apellido"])
                nuevo_nombre = st.text_input("Nuevo Nombre", value=registro_seleccionado["Nombre"])

                if st.button("Editar"):
                    editar_registro(id_seleccionado, nuevo_apellido.capitalize(), nuevo_nombre.capitalize())
    else:
        if apellido_buscar:
            st.warning("No se encontraron registros con ese apellido.")

elif opcion == "ELIMINAR":
    st.subheader("Buscar y Eliminar Registros")

    apellido_buscar = st.text_input("Buscar por Apellido")
    datos = cargar_datos()

    # Filtrar registros por apellido
    registros_filtrados = [registro for registro in datos if apellido_buscar.capitalize() in registro["Apellido"].capitalize()]

    if registros_filtrados:
        apellidos = [registro["Apellido"] for registro in registros_filtrados]
        apellidos_buscar = st.selectbox("Seleccionar Apellido", options=apellidos)

        if apellidos_buscar:
            registro_seleccionado = next((registro for registro in registros_filtrados if registro["Apellido"] == apellidos_buscar), None)
            if registro_seleccionado:
                id_seleccionado = registro_seleccionado["ID"]

                if st.button("Eliminar"):
                    eliminar_registro(id_seleccionado)
    else:
        if apellido_buscar:
            st.warning("No se encontraron registros con ese apellido.")
