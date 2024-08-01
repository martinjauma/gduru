import streamlit as st
import json
import os
import uuid
from datetime import datetime

# Funciones -------------------------------------------------------

# Función para generar un ID único para cada registro
def generar_id():
    return str(uuid.uuid4())

# Función para cargar los datos desde el archivo JSON
def cargar_datos():
    directorio = "jaon"
    archivo_json = os.path.join(directorio, "datos.json")
    if os.path.exists(archivo_json):
        with open(archivo_json, "r") as archivo:
            try:
                datos = json.load(archivo)
                return datos
            except json.JSONDecodeError:
                st.error("Error al cargar los datos desde el archivo JSON.")
                return []
    else:
        return []

# Función para guardar los datos en el archivo JSON
def guardar_datos(datos):
    directorio = "json"
    archivo_json = os.path.join(directorio, "datos.json")
    with open(archivo_json, "w") as archivo:
        json.dump(datos, archivo, indent=4)

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

# ----------------------------------------------------------
st.image("img/uruLogo.jpeg")
# Configurar la interfaz de usuario
st.title("Sistema de Gestión de Registros")

opcion = st.selectbox("Selecciona una opción:", ["ALTA", "EDICIÓN", "ELIMINAR"])

if opcion == "ALTA":
    st.subheader("Formulario de Alta")

    # Lista de campos del formulario
    campos_formulario = ["Apellido", "Nombre", "Edad", "Dirección", "Teléfono", "Email","ALTURA"]

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

            # Cargar datos existentes y agregar nuevos datos
            datos_existentes = cargar_datos()
            datos_existentes.append(datos)
            guardar_datos(datos_existentes)
            
            # Mensaje de éxito
            st.success(f"Formulario enviado con éxito. Los datos se han guardado en la base de datos.")
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
