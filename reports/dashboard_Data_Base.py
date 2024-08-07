import streamlit as st
import pymongo
import pandas as pd
import altair as alt

# Conexión a MongoDB
client = pymongo.MongoClient("mongodb+srv://martinjauma:Piston@clustergd.qny9kpp.mongodb.net/")
db = client["gestDep_db_json"]
collection = db["match_URU"]

# Función para obtener valores únicos de un campo
@st.cache_data
def obtener_valores_unicos(campo):
    return collection.distinct(campo)

# Función para cargar los datos filtrados
@st.cache_data
def cargar_datos_filtrados(fecha, row_name, equipo, resultado):
    filtro = {}
    if fecha:
        filtro["FECHA"] = fecha
    if row_name:
        row_name_mayusculas = [value.upper() for value in row_name]
        filtro["Row Name"] = {"$regex": "|".join(row_name_mayusculas), "$options": "i"}  # Búsqueda case-insensitive
    if equipo:
        filtro["EQUIPO"] = equipo
    if resultado:
        resultado_mayusculas = [value.upper() for value in resultado]
        filtro["RESULTADO"] = {"$regex": "|".join(resultado_mayusculas), "$options": "i"}  # Búsqueda case-insensitive

    # Imprimir la consulta para depuración
    print(filtro)

    return list(collection.find(filtro))



# Título de la aplicación
st.title("Dashboard de Matches URU")

# Obtener valores únicos para todos los filtros

valores_unicos_fecha = obtener_valores_unicos("FECHA")
valores_unicos_row_name = obtener_valores_unicos("Row Name")
valores_unicos_equipo = obtener_valores_unicos("EQUIPO")
valores_unicos_resultado = obtener_valores_unicos("RESULTADO")

# Crear filtros interactivos
fecha_seleccionada = st.selectbox("Selecciona una fecha", valores_unicos_fecha)
row_name_seleccionado = st.multiselect("Selecciona uno o varios ROW NAME", valores_unicos_row_name)
equipo_seleccionado = st.selectbox("Selecciona un equipo", valores_unicos_equipo)
resultado_seleccionado = st.multiselect("Selecciona uno o varios resultados", valores_unicos_resultado)

# Cargar y mostrar los datos filtrados
if fecha_seleccionada or row_name_seleccionado or equipo_seleccionado or resultado_seleccionado:
    datos_filtrados = cargar_datos_filtrados(fecha_seleccionada, row_name_seleccionado, equipo_seleccionado, resultado_seleccionado)
    if datos_filtrados:
        df_filtrados = pd.DataFrame(datos_filtrados)
        st.dataframe(df_filtrados)

        # Crear un gráfico de barras interactivo
        chart = alt.Chart(df_filtrados).mark_bar().encode(
            x='EQUIPO',
            y='count()',
            color='RESULTADO'  # Colorear las barras por resultado
        ).interactive()
        st.altair_chart(chart, use_container_width=True)
    else:
        st.write("No se encontraron registros para los filtros seleccionados.")
else:
    st.write("Por favor, selecciona al menos un filtro.")
