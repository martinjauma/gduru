import pandas as pd
import re
import streamlit as st
from db import get_db
from PIL import Image
import requests
from io import BytesIO

db = get_db()
collection = db["match_URU"]

@st.cache_resource
def obtener_fechas_unicas():
    return collection.distinct('FECHA')

def cargar_datos(fecha):
    return list(collection.find({"FECHA": fecha}))

def cargar_logo(equipo):
    url = f'https://storage.googleapis.com/slar2024/TEROS/TEAMS_strea/{equipo}.png'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza un error si la solicitud falla
        image = Image.open(BytesIO(response.content))
        return image
    except requests.exceptions.RequestException as e:
        st.error(f"Error al cargar la imagen desde la URL: {e}")
        return None
    except Exception as e:
        st.error(f"Error al procesar la imagen: {e}")
        return None
    
# Cargar logo desde gir carpeta images/ ojo que no se alinean los logos si es desde aca
# def cargar_logo(equipo):
#     logo_path = os.path.join('images/', f'{equipo}.png')
#     if os.path.exists(logo_path):
#         return Image.open(logo_path)
#     else:
#         st.error(f"Imagen no encontrada para el equipo: {equipo}")

def procesar_datos(partidos):
    df = pd.DataFrame(partidos)
    if not df.empty:
        regex = r"(\d{6})-(\w{3})-P(\d{2})-(\w{3})@(\w{3})"
        
        def extraer_informacion_fecha(fecha):
            match = re.search(regex, fecha)
            if match:
                return match.groups()
            else:
                return [None] * 5

        df[['FECHA_EXTRAIDA', 'TORNEO', 'PARTIDO', 'LOCAL', 'VISITA']] = df['FECHA'].apply(
            lambda fecha: pd.Series(extraer_informacion_fecha(fecha))
        )

        def determinar_condicion(row):
            equipo, local, visita = row.get('EQUIPO', ''), row.get('LOCAL', ''), row.get('VISITA', '')
            if equipo == "01-URU" and local == "URU":
                return "LOCAL"
            elif equipo == "02-FRA" and visita == "FRA":
                return "VISITA"
            elif equipo == "03-ARG" and visita == "ARG":
                return "VISITA"
            elif equipo == "04-ESC" and visita == "ESC":
                return "VISITA"
            return "UNKNOWN"

        df['CONDICION'] = df.apply(determinar_condicion, axis=1)

        def calcular_puntaje(row, condicion):
            row_name, resultado = row.get('Row Name', ''), row.get('RESULTADO', '')
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

        df['SCORE LOCAL'] = df.apply(lambda row: calcular_puntaje(row, 'LOCAL'), axis=1)
        df['SCORE VISITA'] = df.apply(lambda row: calcular_puntaje(row, 'VISITA'), axis=1)
        
        return df
    return pd.DataFrame()

# Obtener fechas únicas para el selector
fechas_disponibles = obtener_fechas_unicas()
fecha_seleccionada = st.selectbox('Seleccionar un Match:', fechas_disponibles)

if fecha_seleccionada:
    partidos = cargar_datos(fecha_seleccionada)
    df_filtrado = procesar_datos(partidos)

    if not df_filtrado.empty:
        total_score_local = df_filtrado['SCORE LOCAL'].sum()
        total_score_visita = df_filtrado['SCORE VISITA'].sum()

        # Crear interfaz en Streamlit
        st.title('SCORE')

        # Crear dos columnas para los logos
        col1, col2, col3 = st.columns(3)

        # En la primera columna, mostrar el logo local
        with col1:
            st.markdown(f"""
                <div style='display: flex; flex-direction: column; justify-content: flex-end; height: 200px;'>
                    <img src='https://storage.googleapis.com/slar2024/TEROS/TEAMS_strea/{df_filtrado["LOCAL"].iloc[0]}.png' width='150' />
                    <p style='text-align: center;'>{df_filtrado["LOCAL"].iloc[0]}</p>
                </div>
                """, unsafe_allow_html=True)

        # En la segunda columna, dejar espacio
        with col2:
            st.write("")

        # En la tercera columna, mostrar el logo visitante
        with col3:
            st.markdown(f"""
                <div style='display: flex; flex-direction: column; justify-content: flex-end; height: 200px;'>
                    <img src='https://storage.googleapis.com/slar2024/TEROS/TEAMS_strea/{df_filtrado["VISITA"].iloc[0]}.png' width='150' />
                    <p style='text-align: center;'>{df_filtrado["VISITA"].iloc[0]}</p>
                </div>
                """, unsafe_allow_html=True)

        # Crear dos columnas para los puntajes
        col1, col2, col3 = st.columns(3)

        # Mostrar el puntaje local
        with col1:
            st.markdown(f"""
                <div style='text-align: center;'>
                    <h2 style='font-size: 24px;'>Score Local</h2>
                    <h1 style='font-size: 36px;'>{total_score_local}</h1>
                </div>
                """, unsafe_allow_html=True)

        # Dejar espacio en la segunda columna
        with col2:
            st.write("")

        # Mostrar el puntaje visitante
        with col3:
            st.markdown(f"""
                <div style='text-align: center;'>
                    <h2 style='font-size: 24px;'>Score Visita</h2>
                    <h1 style='font-size: 36px;'>{total_score_visita}</h1>
                </div>
                """, unsafe_allow_html=True)

        st.write("---")
        
        st.subheader('Tabla del Partido Seleccionado')

        # Mostrar la tabla de datos en un expander
        with st.expander("Datos del Partido"):
            st.dataframe(df_filtrado)
