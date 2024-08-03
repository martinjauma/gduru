import streamlit as st
import pymongo
import pandas as pd

# Conexión a MongoDB
client = pymongo.MongoClient("mongodb+srv://martinjauma:Piston@clustergd.qny9kpp.mongodb.net/")
db = client["gestDep_db_json"]
collection = db["match_URU"]

# Función para cargar todos los datos de la colección
@st.cache_data
def cargar_todos_los_datos():
    return list(collection.find())

# Función para obtener valores únicos de la clave "FECHA"
@st.cache_data
def obtener_valores_unicos_fecha():
    return collection.distinct("FECHA")

# Función para cargar los datos filtrados por fecha
@st.cache_data
def cargar_datos_por_fecha(fecha):
    return list(collection.find({"FECHA": fecha}))

# Mostrar tabla con todos los datos de la colección
st.title("Todos los Registros en la Base de Datos")
st.subheader("Match URU")

# Obtener y mostrar valores únicos de la clave "FECHA"
valores_unicos_fecha = obtener_valores_unicos_fecha()
fecha_seleccionada = st.selectbox("Selecciona una fecha", valores_unicos_fecha)

# Cargar y mostrar los datos filtrados por fecha
if fecha_seleccionada:
    datos_filtrados = cargar_datos_por_fecha(fecha_seleccionada)
    if datos_filtrados:
        df_filtrados = pd.DataFrame(datos_filtrados)
        st.dataframe(df_filtrados)
    else:
        st.write("No se encontraron registros para la fecha seleccionada.")
else:
    st.write("Por favor, selecciona una fecha para mostrar los registros.")
