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
    # Si no se selecciona ninguna ciudad, usar todos los códigos postales
    codigos_postales_disponibles = df['Zipcode'].unique()

# Convertir los códigos postales disponibles a texto para mostrar en el placeholder
placeholder_codigos_postales = ", ".join(map(str, codigos_postales_disponibles))

# Bloque 2: Filtro por Códigos Postales (como entrada de texto)
st.header("Filtro por Códigos Postales")
st.write("Ingresa los códigos postales separados por comas (Ejemplo: 4006, 4004, 37004)")
input_zipcodes = st.text_input('Códigos postales', placeholder_codigos_postales)  # Mostrar solo los códigos relevantes

# Convertir los códigos postales ingresados en una lista de enteros
try:
    zipcodes_a_buscar = [int(zipcode.strip()) for zipcode in input_zipcodes.split(',')]
except ValueError:
    st.write("Por favor, asegúrate de que todos los códigos postales sean números separados por comas.")
    zipcodes_a_buscar = []

# Filtrar el DataFrame en función de los filtros seleccionados
df_filtrado_final = df.copy()

# Aplicar filtro de ciudad si hay ciudades seleccionadas
if ciudades_seleccionadas:
    df_filtrado_final = df_filtrado_final[df_filtrado_final['City'].isin(ciudades_seleccionadas)]

# Aplicar filtro de código postal si hay códigos postales ingresados
if zipcodes_a_buscar:
    df_filtrado_final = df_filtrado_final[df_filtrado_final['Zipcode'].isin(zipcodes_a_buscar)]

# Seleccionar solo las columnas que necesitas para el resultado
df_resultado = df_filtrado_final[['Zipcode', 'Frame id', 'Full address', 'Publisher', 'City', 'Venue types']]

# Mostrar resultados en función de los filtros aplicados
if not df_resultado.empty:
    st.write("Resultados encontrados con los filtros aplicados:")
    st.dataframe(df_resultado)
else:
    st.write("No se encontraron resultados para los filtros seleccionados.")
