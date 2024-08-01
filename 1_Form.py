import streamlit as st
import pymongo
from datetime import datetime

# Conexión a MongoDB
client = pymongo.MongoClient("mongodb+srv://martinjauma:pistonAdmin@cluster0.g4mk1az.mongodb.net/")
db = client["gestDep"]
collection = db["bd_JSON"]

# Función para generar un ID único para cada registro
def generar_id():
    return str(uuid.uuid4())

# ... (resto del código, sin las funciones de cargar_datos y guardar_datos)

if submit_button:
    # Crear un diccionario con los datos del formulario
    new_user = {
        "ID": generar_id(),
        "FechaAlta": datetime.now().strftime("%Y%m%d%H:%M"),
        "Apellido": datos_formulario["Apellido"].capitalize(),
        # ... otros campos
    }

    # Insertar el documento en MongoDB
    result = collection.insert_one(new_user)
    st.success(f"Formulario enviado con éxito. ID del registro: {result.inserted_id}")

# ... (resto del código, modificando las funciones de edición y eliminación para usar MongoDB)

def editar_registro(id_unico, nuevo_apellido, nuevo_nombre):
    # Busca el documento por ID y actualiza los campos
    result = collection.update_one({"ID": id_unico}, {"$set": {"Apellido": nuevo_apellido.capitalize(), "Nombre": nuevo_nombre.capitalize()}})
    if result.modified_count > 0:
        st.success(f"Registro con ID {id_unico} actualizado correctamente.")
    else:
        st.warning(f"No se encontró ningún registro con ID {id_unico}")

def eliminar_registro(id_unico):
    # Elimina el documento por ID
    result = collection.delete_one({"ID": id_unico})
    if result.deleted_count > 0:
        st.success(f"Registro con ID {id_unico} eliminado correctamente.")
    else:
        st.warning(f"No se encontró ningún registro con ID {id_unico}")
