import pandas as pd
from pymongo import MongoClient
import re
import streamlit as st

# Conexión a MongoDB
client = MongoClient("mongodb+srv://martinjauma:Piston@clustergd.qny9kpp.mongodb.net/")
db = client["gestDep_db_json"]
collection = db["match_URU"]

# Extraer datos de MongoDB
partidos = list(collection.find())
df = pd.DataFrame(partidos)

# Verificar las columnas del DataFrame
# st.write("Columnas del DataFrame:", df.columns)

# Procesar datos
def extraer_informacion_fecha(fecha):
    regex = r"(\d{6})-(\w{3})-P(\d{2})-(\w{3})@(\w{3})"
    match = re.search(regex, fecha)
    if match:
        date, torneo, partido, equipo_local, equipo_visitante = match.groups()
        return date, torneo, partido, equipo_local, equipo_visitante
    else:
        return None, None, None, None, None

# Aplicar la función de extracción de fecha
if 'FECHA' in df.columns:
    df[['FECHA_EXTRAIDA', 'TORNEO', 'PARTIDO', 'LOCAL', 'VISITA']] = df['FECHA'].apply(
        lambda fecha: pd.Series(extraer_informacion_fecha(fecha))
    )
else:
    st.error("La columna 'FECHA' no se encuentra en el DataFrame.")

def determinar_condicion(row):
    equipo = row.get('EQUIPO', '')
    local = row.get('LOCAL', '')
    visita = row.get('VISITA', '')

    if equipo == "01-URU" and local == "URU":
        return "LOCAL"
    elif equipo == "02-FRA" and visita == "FRA":
        return "VISITA"
    elif equipo == "03-ARG" and visita == "ARG":
        return "VISITA"
    elif equipo == "04-ESC" and visita == "ESC":
        return "VISITA"
    return "UNKNOWN"

if 'LOCAL' in df.columns and 'VISITA' in df.columns:
    df['CONDICION'] = df.apply(determinar_condicion, axis=1)
else:
    st.error("Las columnas 'LOCAL' y 'VISITA' no se encuentran en el DataFrame.")

@st.cache_data
def calcular_puntaje(row, condicion):
    row_name = row.get('Row Name', '')
    resultado = row.get('RESULTADO', '')
    if row_name == "TRY" and row['CONDICION'] == condicion:
        return 5
    elif row_name == "TRY PENAL" and row['CONDICION'] == condicion:
        return 7
    elif row_name == "GOAL" and resultado == "CONVERTIDO" and row['CONDICION'] == condicion:
        return 2
    elif row_name == "PENALTY KICK" and resultado == "CONVERTIDO" and row['CONDICION'] == condicion:
        return 3
    elif row_name == "DROP" and resultado == "CONVERTIDO" and row['CONDICION'] == condicion:
        return 3
    return 0

if 'CONDICION' in df.columns:
    df['SCORE LOCAL'] = df.apply(lambda row: calcular_puntaje(row, 'LOCAL'), axis=1)
    df['SCORE VISITA'] = df.apply(lambda row: calcular_puntaje(row, 'VISITA'), axis=1)

# Selector único de FECHA
fechas_disponibles = df['FECHA'].unique()
# Para el título grande
st.markdown('<h1 style="font-size: 30px;">MATCH</h1>', unsafe_allow_html=True)

fecha_seleccionada = st.selectbox('Seleccionar un Match:', fechas_disponibles)

# Filtrar DataFrame por la fecha seleccionada
df_filtrado = df[df['FECHA'] == fecha_seleccionada]

total_score_local = df_filtrado['SCORE LOCAL'].sum()
total_score_visita = df_filtrado['SCORE VISITA'].sum()

# Crear interfaz en Streamlit
st.title('SCORE')

# Crear dos columnas
col1, col2 = st.columns(2)

# En la primera columna, mostrar el primer metric
with col1:
    st.markdown(f'<h2 style="font-size: 24px;">{df_filtrado["LOCAL"].iloc[0]}</h2>', unsafe_allow_html=True)
    st.metric(label="", value=total_score_local)

# En la segunda columna, mostrar el segundo metric
with col2:
    st.markdown(f'<h2 style="font-size: 24px;">{df_filtrado["VISITA"].iloc[0]}</h2>', unsafe_allow_html=True)
    st.metric(label="", value=total_score_visita)


st.subheader('Tabla del Partido Selecionado')

# Colapsar tabla de datos en un expander
with st.expander("Datos del Partido"):
    st.dataframe(df_filtrado)