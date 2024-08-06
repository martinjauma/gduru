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

st.write('REPORTE INDIVIDALES PROXIMAMENTE')

