

import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium

from folium.plugins import Search

# Paso 1: Cargar el CSV en un DataFrame de pandas
ruta_csv = 'DOOH  15 - Sheet1.csv'  # Cambia esta ruta al archivo CSV que tienes
df = pd.read_csv(ruta_csv)

# Convertir Latitude y Longitude a números, ignorando valores no válidos
df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')

# Eliminar filas con coordenadas inválidas
df = df.dropna(subset=['Latitude', 'Longitude'])

# Paso 2: Preprocesamiento del DataFrame
df.fillna(0, inplace=True)
df['Zipcode'] = df['Zipcode'].astype(float).astype(int)

st.title('Búsqueda de Información DOOH')

# Bloque 1: Filtro por Ciudad (con multiselección)
st.header("Filtro por Ciudad")
ciudades_disponibles = df['City'].unique()  # Lista de todas las ciudades
ciudades_seleccionadas = st.multiselect("Selecciona una o varias ciudades", ciudades_disponibles)

# Filtrar venue types disponibles en función de las ciudades seleccionadas
if ciudades_seleccionadas:
    df_filtrado_por_ciudad = df[df['City'].isin(ciudades_seleccionadas)]
    venuetypes_disponibles = df_filtrado_por_ciudad['Venue types'].unique()
else:
    # Si no se selecciona ninguna ciudad, mostrar todos los venue types
    venuetypes_disponibles = df['Venue types'].unique()

# Bloque 2: Filtro por Venue type (dependiente del filtro de ciudad)
st.header("Filtro por Venue types")
venuetypes_seleccionados = st.multiselect("Selecciona uno o varios Venue types. Outdoor= exterior, subway=estaciones de tren, parking/garages y malls= Centros Comerciales", venuetypes_disponibles)

# Filtrar el DataFrame en función de los filtros seleccionados
df_filtrado_final = df.copy()

# Aplicar filtro de ciudad si hay ciudades seleccionadas
if ciudades_seleccionadas:
    df_filtrado_final = df_filtrado_final[df_filtrado_final['City'].isin(ciudades_seleccionadas)]

# Aplicar filtro de venue type si hay venue types seleccionados
if venuetypes_seleccionados:
    df_filtrado_final = df_filtrado_final[df_filtrado_final['Venue types'].isin(venuetypes_seleccionados)]

# Seleccionar solo las columnas que necesitas para el resultado
df_resultado = df_filtrado_final[['Zipcode', 'Frame id', 'Full address', 'Publisher', 'City', 'Venue types', 'Latitude', 'Longitude']]

# Mostrar resultados en función de los filtros aplicados
if not df_resultado.empty:
    st.write("Resultados encontrados con los filtros aplicados:")
    st.dataframe(df_resultado)

    # Crear un mapa interactivo con Folium
    st.header("Mapa de Ubicaciones")
    centro_mapa = [df_resultado['Latitude'].mean(), df_resultado['Longitude'].mean()]
    mapa = folium.Map(location=centro_mapa, zoom_start=16)
  # Crear un grupo de marcadores para el buscador
    marker_group = folium.FeatureGroup(name="Marcadores")
    mapa.add_child(marker_group)

    # Agregar marcadores al mapa como puntos individuales
    for _, row in df_resultado.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"{row['Full address']} - {row['Venue types']}",
            tooltip=row['City']
        ).add_to(marker_group)

    # Agregar un buscador de ubicaciones
    search = Search(
        layer=marker_group,  # Buscar en los marcadores individuales
        search_label='City',   # Buscar por la columna 'City'
        placeholder='Buscar ciudad...',
        collapsed=True
    ).add_to(mapa)

    # Mostrar el mapa en Streamlit
    st_folium(mapa, width=700, height=500)
     # Guardar el mapa en un archivo HTML
    mapa.save("mapa_interactivo.html")

    # Botón para descargar el mapa como HTML
    with open("mapa_interactivo.html", "rb") as file:
        btn = st.download_button(
            label="Descargar Mapa (HTML)",
            data=file,
            file_name="mapa_interactivo.html",
            mime="text/html"
        )
else:
    st.write("No se encontraron resultados para los filtros seleccionados.")

# Bloque 3: Búsqueda por Códigos Postales
st.header("Búsqueda por Códigos Postales (No aplicable filtros de Ciudad y Venue)")
st.write("Ingresa los códigos postales separados por comas (Ejemplo: 4006, 4004, 37004)")

# Caja de texto para ingresar los códigos postales
input_zipcodes = st.text_input('Códigos postales', '4006, 4004, 37004')  # Valor por defecto

# Convertir los códigos postales ingresados en una lista de enteros
zipcodes_a_buscar = [int(zipcode.strip()) for zipcode in input_zipcodes.split(',')]
# Filtrar el DataFrame por códigos postales
df_filtrado_zip = df[df['Zipcode'].isin(zipcodes_a_buscar)]

# Seleccionar solo las columnas que necesitas para el resultado
df_resultado_zip = df_filtrado_zip[['Zipcode', 'Frame id', 'Full address', 'Publisher', 'City', 'Venue types']]

# Mostrar resultados del bloque de códigos postales
if not df_resultado_zip.empty:
    st.write("Resultados encontrados por códigos postales:")
    st.dataframe(df_resultado_zip)
else:
    st.write("No se encontraron resultados para los códigos postales ingresados.")




