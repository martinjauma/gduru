import streamlit as st
import pymongo
from datetime import datetime
import uuid 

# Conexión a MongoDB
client = pymongo.MongoClient("mongodb+srv://martinjauma:Piston@clustergd.qny9kpp.mongodb.net/") 
db = client["gestDep_db_json"]
collection = db["gest_dep_ALTA"]

# Función para generar un ID único para cada registro
def generar_id():
    return str(uuid.uuid4())

# Función para buscar registros por apellido
def buscar_registros_por_apellido(apellido):
    return collection.find({"Apellido": apellido.capitalize()})

# Función para editar un registro por ID
def editar_registro(id_unico, nuevo_apellido, nuevo_nombre):
    result = collection.update_one({"ID": id_unico}, {"$set": {"Apellido": nuevo_apellido.capitalize(), "Nombre": nuevo_nombre.capitalize()}})
    if result.modified_count > 0:
        st.success(f"Registro con ID {id_unico} actualizado correctamente.")
    else:
        st.warning(f"No se encontró ningún registro con ID {id_unico}")

# Función para eliminar un registro por ID
def eliminar_registro(id_unico):
    result = collection.delete_one({"ID": id_unico})
    if result.deleted_count > 0:
        st.success(f"Registro con ID {id_unico} eliminado correctamente.")
    else:
        st.warning(f"No se encontró ningún registro con ID {id_unico}")

# ----------------------------------------------------------
st.logo("img/uruLogo.png")
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
            nuevo_registro = {
                "ID": id_unico,
                "FechaAlta": fecha_alta
            }
            
            # Agregar datos del formulario al diccionario
            for campo, valor in datos_formulario.items():
                nuevo_registro[campo] = valor.capitalize()

            # Insertar el documento en MongoDB
            result = collection.insert_one(nuevo_registro)
            st.success(f"Formulario enviado con éxito. ID del registro: {result.inserted_id}")
        else:
            st.error("Por favor, complete todos los campos.")

elif opcion == "EDICIÓN":
    st.subheader("Buscar y Editar Registros")

    apellido_buscar = st.text_input("Buscar por Apellido")
    resultados = buscar_registros_por_apellido(apellido_buscar)

    if resultados.count() > 0:
        registros = list(resultados)
        apellidos = [registro["Apellido"] for registro in registros]
        apellidos_buscar = st.selectbox("Seleccionar Apellido", options=apellidos)

        if apellidos_buscar:
            registro_seleccionado = next((registro for registro in registros if registro["Apellido"] == apellidos_buscar), None)
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
