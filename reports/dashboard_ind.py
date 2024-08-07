import pandas as pd
import streamlit as st
from db import get_db  # Importamos la función para obtener la conexión a la base de datos
import plotly.express as px

# Conectar a la base de datos
db = get_db()
collection = db["ind_URU"]

# Función para cargar todos los datos de la colección
@st.cache_resource
def cargar_todos_los_datos():
    return list(collection.find({}))

# Cargar los datos
datos = cargar_todos_los_datos()

# Procesar los datos en un DataFrame
df = pd.DataFrame(datos)

# Función para renombrar los Row Names
def renombrar_row_name(row_name):
    if row_name in ["P1 - Pase  Pos", "P2 - Pase Neg", "PL - Offload", "PM - Pelota  en mano", "PO - Recep  Aerea Pos", "PQ - Recep  Aerea Levantada", "PR - Perdidas", "PT + Pie Pos", "PT - Pie Neg", "Q9 - Maul  Ataque", "QP Presentacion Pos","QP Presentacion +","QP Presentacion -", "QP Presentacion NEG", "QR + 1o Ruck Ata POS", "QR + 2o Ruck Ata POS", "QR + 3o Ruck Ata POS", "QR - 1o Ruck Ata NEG", "QR - 2o Ruck Ata NEG", "QR - 3o Ruck Ata NEG"]:
        return "ACC ATAQUE"
    elif row_name in ["D1 - TA Pos", "D2 - Tackle", "D3 - TA Asist +", "D4 - TA Asist", "D5 - TA Off Load", "D6 - TA Err", "D7 - Pescada", "D8 - Recuperada", "D9 - Maul  Defensivo", "DC - Contest  Aereo +", "DC - Contest  Aereo -", "DR + 1o Ruck Def  POS", "DR + 2o Ruck Def  POS", "DR + 3o Ruck Def  POS", "DR - 1o Ruck Def  NEG", "DR - 2o Ruck Def  NEG", "DR - 3o Ruck Def  NEG"]:
        return "ACC DEFENSIVAS"
    elif row_name in ["R1 Penal", "R2 Duelo Gan", "R3 Duelo Emp", "R4 Duelo Per", "R5 Try", "R6 Conversion +", "R7 Conversion -", "S1 - Pase + Medio", "S2 - Pase - Medio", "S3 Patada +  Especialista", "S4 Patada - Especialista", "T1 Scrum +", "T1 Scrum -", "T2 Line +", "T2 Line -", "T3 Lanzamiento  Line +", "T3 Lanzamiento  Line -"]:
        return "ACC ESPECIALES"
    else:
        return "OTRO"

# Aplicar la función para renombrar los Row Names
df['Grupo Row Name'] = df['Row Name'].apply(renombrar_row_name)

# Interfaz de Streamlit
st.title('REPORTE INDIVIDUALES PROXIMAMENTE')

# Seleccionar una o varias fechas
fechas_disponibles = df['FECHA'].unique()
fechas_seleccionadas = st.multiselect('Seleccionar una o varias fechas:', fechas_disponibles)

# Seleccionar un nombre
nombres_disponibles = df['NOMBRE'].unique()
nombre_seleccionado = st.selectbox('Seleccionar un nombre:', nombres_disponibles)

# Filtrar los datos
if fechas_seleccionadas:
    df = df[df['FECHA'].isin(fechas_seleccionadas)]
if nombre_seleccionado:
    df = df[df['NOMBRE'] == nombre_seleccionado]

# Crear tablas para cada grupo
grupo_acc_atq = df[df['Grupo Row Name'] == 'ACC ATAQUE']
grupo_acc_def = df[df['Grupo Row Name'] == 'ACC DEFENSIVAS']
grupo_acc_esp = df[df['Grupo Row Name'] == 'ACC ESPECIALES']

# Contar los Row Names dentro de cada grupo
conteo_atq = grupo_acc_atq['Row Name'].value_counts().reset_index()
conteo_atq.columns = ['ACC IND', '#']

conteo_def = grupo_acc_def['Row Name'].value_counts().reset_index()
conteo_def.columns = ['ACC IND', '#']

conteo_esp = grupo_acc_esp['Row Name'].value_counts().reset_index()
conteo_esp.columns = ['ACC IND', '#']

# Crear función para convertir tabla a HTML sin índice
def table_to_html(df):
    return df.to_html(index=False)

# Crear gráficos de radar
def crear_grafico_radar(df, title):
    fig = px.line_polar(df, r='#', theta='ACC IND', line_close=True, title=title)
    fig.update_traces(fill='toself')
    fig.update_layout(polar=dict(radialaxis=dict(visible=True)))
    return fig

# Contar los grupos
conteo_grupos = df['Grupo Row Name'].value_counts().reset_index()
conteo_grupos.columns = ['Grupo Row Name', 'Conteo']

# Crear gráfico de radar para los grupos
def crear_grafico_radar_grupos(df, title):
    fig = px.line_polar(df, r='Conteo', theta='Grupo Row Name', line_close=True, title=title)
    fig.update_traces(fill='toself')
    fig.update_layout(polar=dict(radialaxis=dict(visible=True)))
    return fig

st.write('---')


# Mostrar las tablas y gráficos en tres columnas
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader('ACC ATAQUE')
    st.write(table_to_html(conteo_atq), unsafe_allow_html=True)
    st.markdown(f'<div style="text-align: left; font-size: 24px;"><strong>Total ACC ATQ:</strong> {len(grupo_acc_atq)}</div>', unsafe_allow_html=True)

with col2:
    st.subheader('ACC DEFENSIVAS')
    st.write(table_to_html(conteo_def), unsafe_allow_html=True)
    st.markdown(f'<div style="text-align: left; font-size: 24px;"><strong>Total ACC DEF:</strong> {len(grupo_acc_def)}</div>', unsafe_allow_html=True)

with col3:
    st.subheader('ACC ESPECIALES')
    st.write(table_to_html(conteo_esp), unsafe_allow_html=True)
    st.markdown(f'<div style="text-align: left; font-size: 24px;"><strong>Total ACC ESP:</strong> {len(grupo_acc_esp)}</div>', unsafe_allow_html=True)




st.write('---')
col1,col2 = st.columns([1,2])
# Mostrar la tabla de conteo y gráfico de radar para los grupos

with col1:
    st.subheader('ACC Seleccionadas')
    st.table(df['Grupo Row Name'].value_counts().reset_index().rename(columns={'index': 'ACC', 'Grupo Row Name': '#'}))

with col2:
    st.plotly_chart(crear_grafico_radar_grupos(conteo_grupos, ''), use_container_width=True)

# # Filtrar los datos que se clasifican como 'OTRO'
# otros_row_names = df[df['Grupo Row Name'] == 'OTRO']['Row Name'].unique()

# # # Mostrar los Row Names que están clasificados como 'OTRO'
# # st.write('Row Names clasificados como OTRO:')
# # st.write(otros_row_names)