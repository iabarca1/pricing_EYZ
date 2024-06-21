import streamlit as st
import pandas as pd
import numpy as np
import pyodbc
import json

# Leer el archivo de secrets
database_config = st.secrets["database"]

# Función para ejecutar todos los scrapers
def run_all_scrapers():
    import run_all_scrapers
    return run_all_scrapers.execute()

# Leer el diccionario de homologación desde el archivo JSON
with open('/mnt/data/Diccionario_homolagcion.json') as f:
    homologacion_data = json.load(f)

# Convertir el diccionario de homologación a DataFrame
homologacion_df = pd.DataFrame(homologacion_data)

# Conectar a la base de datos usando pyodbc
conn_str = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={database_config['server']};"
    f"DATABASE={database_config['database']};"
    f"UID={database_config['username']};"
    f"PWD={database_config['password']}"
)
conn = pyodbc.connect(conn_str)

# Realizar la consulta SQL para obtener datos de productos
query = """
SELECT
    precios.[KOPR] as Id_SKU,
    maestro.NOKOPR,
    precios.[PP02UD] as Precio_EYZ
FROM [BARRACA].[dbo].[TABPRE] as precios
LEFT JOIN MAEPR as maestro on precios.KOPR = maestro.KOPR
WHERE KOLT='01P'
"""
productos_df = pd.read_sql_query(query, conn)

# Cerrar la conexión a la base de datos
conn.close()

# Obtener datos de los scrapers
datos_scrapers = run_all_scrapers()

# Convertir datos de scrapers a DataFrame
scraper_dfs = []
for nombre_scraper, datos in datos_scrapers.items():
    df = pd.DataFrame(datos)
    df['nombre'] = df['nombre'].map(homologacion_df.set_index(f'Nombre {nombre_scraper}')['Nombre_SKU'])
    df['scraper'] = nombre_scraper
    scraper_dfs.append(df)

# Concatenar todos los datos en un solo DataFrame
scrapers_combined_df = pd.concat(scraper_dfs)

# Función para calcular la diferencia de precios
def calcular_diferencia(producto_base, productos_scrapers):
    diferencias = []
    for _, producto in productos_scrapers.iterrows():
        if producto['Id_SKU'] == producto_base['Id_SKU']:
            diferencia = ((producto['precio'] - producto_base['Precio_EYZ']) / producto_base['Precio_EYZ']) * 100
            diferencias.append(diferencia)
    return diferencias

# Interfaz de Streamlit
st.title("Comparación de Precios de Productos")

# Tabla con diferencias de precios
st.header("Diferencias de Precios")
diferencias_data = []

for _, producto_base in productos_df.iterrows():
    diferencias = calcular_diferencia(producto_base, scrapers_combined_df)
    if diferencias:
        promedio_diferencia = np.mean(diferencias)
    else:
        promedio_diferencia = np.nan
    diferencias_data.append({
        'ID Producto': producto_base['Id_SKU'],
        'Nombre Producto': producto_base['NOKOPR'],
        'Precio Base': producto_base['Precio_EYZ'],
        'Promedio Diferencia de Precio (%)': promedio_diferencia
    })

diferencias_df = pd.DataFrame(diferencias_data)
st.dataframe(diferencias_df)

# Tablas por scraper
st.header("Datos por Scraper")
for nombre_scraper, df in scrapers_combined_df.groupby('scraper'):
    st.subheader(f"Datos de {nombre_scraper}")
    st.dataframe(df[['Id_SKU', 'nombre', 'precio']])
