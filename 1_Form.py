import streamlit as st
import json
import os
import uuid
from datetime import datetime
from pymongo import MongoClient
import pandas as pd

# Conexión a MongoDB
client = MongoClient("mongodb://tu_usuario:tu_contraseña@tu_host:tu_puerto")
db = client["nombre_de_tu_base_de_datos"]
collection = db["nombre_de_tu_colección"]

# Funciones -------------------------------------------------------

# Función para generar un ID único para cada registro
def generar_id():
    return str(uuid.uuid4())

# Función para cargar los datos desde MongoDB
def cargar_datos():
    return list(collection.find())

# Función para guardar los datos en MongoDB
def guardar_datos(datos):
    collection.insert_one(datos)

# Función para eliminar un registro por ID
def eliminar_registro(id_unico):
    result = collection.delete_one({"ID": id_unico})
    if result.deleted_count > 0:
        st.success("Registro eliminado correctamente.")
    else:
        st.warning("No se encontró el registro con ID {id_unico}.")

# Función para editar un registro por ID
def editar_registro(id_unico, nuevo_apellido, nuevo_nombre):
    result = collection.update_one(
        {"ID": id_unico},
        {"$set": {"Apellido": nuevo_apellido.capitalize(), "Nombre": nuevo_nombre.capitalize()}}
    )
    if result.modified_count > 0:
        st.success("Registro editado correctamente.")
    else:
        st.warning("No se encontró el registro con ID {id_unico}.")

# ----------------------------------------------------------

# Configurar la interfaz de usuario
st.title("Sistema de Gestión de Registros")

opcion = st.selectbox("Selecciona una opción:", ["ALTA", "EDICIÓN", "ELIMINAR", "VER DATOS"])

if opcion == "ALTA":
    st.subheader("Formulario de Alta")

    # Lista de campos del formulario
    campos_formulario = ["Apellido", "Nombre", "Edad", "Dirección", "Teléfono", "Email", "ALTURA"]

    with st.form(key='miForm', clear_on_submit=True):
        # Crear inputs dinámicamente
        datos_formulario = {}
        for campo in campos_formulario:
            datos_formulario[campo] = st.text_input(campo)

        submit_button = st.form_submit_button("Alta")

    if submit_button:
        if all(datos_formulario.values()):
            # Generar un ID único
            id_unico = generar_id()

            # Obtener la fecha y hora actuales
            fecha_alta = datetime.now().strftime("%Y%m%d%H:%M")

            # Crear un diccionario con los datos del formulario
            datos = {
                "ID": id_unico,
                "FechaAlta": fecha_alta
            }

            # Agregar datos del formulario al diccionario
            for campo, valor in datos_formulario.items():
                datos[campo] = valor.capitalize()

            # Guardar datos en MongoDB
            guardar_datos(datos)

            # Mensaje de éxito
            st.success("Formulario enviado con éxito. Los datos se han guardado en la base de datos.")
        else:
            st.error("Por favor, complete todos los campos.")

elif opcion == "EDICIÓN":
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
                    editar_registro(id_seleccionado, nuevo_apellido, nuevo_nombre)
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

elif opcion == "VER DATOS":
    st.subheader("Datos de la base de datos")

    datos = cargar_datos()
    df = pd.DataFrame(datos)

    # Mostrar los datos en Streamlit
    st.write(df)
