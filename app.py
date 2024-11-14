import pandas as pd
import streamlit as st

# Paso 1: Cargar el CSV en un DataFrame de pandas
ruta_csv = 'jcdcaux.csv'  # Cambia esta ruta al archivo CSV que tienes
df = pd.read_csv(ruta_csv)

# Paso 2: Preprocesamiento del DataFrame
df.fillna(0, inplace=True)
df['Zipcode'] = df['Zipcode'].astype(float).astype(int)

st.title('Búsqueda de Información con Filtros Dependientes')

# Bloque 1: Filtro por Ciudad (con multiselección)
st.header("Filtro por Ciudad")
ciudades_disponibles = df['City'].unique()  # Lista de todas las ciudades
ciudades_seleccionadas = st.multiselect("Selecciona una o varias ciudades", ciudades_disponibles)

# Filtrar códigos postales disponibles en función de las ciudades seleccionadas
if ciudades_seleccionadas:
    df_filtrado_por_ciudad = df[df['City'].isin(ciudades_seleccionadas)]
    codigos_postales_disponibles = df_filtrado_por_ciudad['Zipcode'].unique()
else:
    # Si no se selecciona ninguna ciudad, mostrar todos los códigos postales
    codigos_postales_disponibles = df['Zipcode'].unique()

# Bloque 2: Filtro por Código Postal (dependiente del filtro de ciudad)
st.header("Filtro por Código Postal")
codigos_postales_seleccionados = st.multiselect("Selecciona uno o varios códigos postales", codigos_postales_disponibles)

# Filtrar el DataFrame en función de los filtros seleccionados
df_filtrado_final = df.copy()

# Aplicar filtro de ciudad si hay ciudades seleccionadas
if ciudades_seleccionadas:
    df_filtrado_final = df_filtrado_final[df_filtrado_final['City'].isin(ciudades_seleccionadas)]

# Aplicar filtro de código postal si hay códigos postales seleccionados
if codigos_postales_seleccionados:
    df_filtrado_final = df_filtrado_final[df_filtrado_final['Zipcode'].isin(codigos_postales_seleccionados)]

# Seleccionar solo las columnas que necesitas para el resultado
df_resultado = df_filtrado_final[['Zipcode', 'Frame id', 'Full address', 'Publisher', 'City', 'Venue types']]

# Mostrar resultados en función de los filtros aplicados
if not df_resultado.empty:
    st.write("Resultados encontrados con los filtros aplicados:")
    st.dataframe(df_resultado)
else:
    st.write("No se encontraron resultados para los filtros seleccionados.")
