import streamlit as st
import pymongo
import pandas as pd

# Conexión a MongoDB
client = pymongo.MongoClient("mongodb+srv://martinjauma:Piston@clustergd.qny9kpp.mongodb.net/")
db = client["gestDep_db_json"]
collection = db["match_URU"]


# Función para cargar todos los datos de la colección
def cargar_todos_los_datos():
    return list(collection.find())




# Mostrar tabla con todos los datos de la colección
st.subheader("Todos los Registros en la Base de Datos")
datos_todos_registros = cargar_todos_los_datos()
df_todos_registros = pd.DataFrame(datos_todos_registros)
st.dataframe(df_todos_registros)