pip install streamlit geopy pandas

import pandas as pd
import streamlit as st
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Paso 1: Cargar el CSV en un DataFrame de pandas
ruta_csv = 'jcdcaux - jcdcaux (1).csv'  # Cambia esta ruta al archivo CSV que tienes
df = pd.read_csv(ruta_csv)

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
df_resultado = df_filtrado_final[['Zipcode', 'Frame id', 'Full address', 'Publisher', 'City', 'Venue types']]

# Mostrar resultados en función de los filtros aplicados
if not df_resultado.empty:
    st.write("Resultados encontrados con los filtros aplicados:")
    st.dataframe(df_resultado)
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

# Configuración de geolocalizador
geolocator = Nominatim(user_agent="geoapp")

# Función para obtener coordenadas
def get_coordinates(address):
    try:
        location = geolocator.geocode(address, timeout=10)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except GeocoderTimedOut:
        return None, None

# Aplicación Streamlit
st.title("Conversor de direcciones a coordenadas")
st.write("Sube un archivo CSV con una columna de direcciones, y obtendrás las coordenadas (latitud y longitud).")

# Cargar archivo CSV
uploaded_file = st.file_uploader("Sube tu archivo CSV", type=["csv"])

if uploaded_file:
    # Leer archivo
    df = pd.read_csv(uploaded_file)

    # Mostrar primeras filas del archivo cargado
    st.write("Vista previa de tus datos:")
    st.dataframe(df.head())

    # Verificar si existe una columna de direcciones
    column_name = st.selectbox("Selecciona la columna con las direcciones:", df.columns)

    if st.button("Obtener coordenadas"):
        st.write("Procesando direcciones, por favor espera...")

        # Crear nuevas columnas para latitud y longitud
        df['Latitud'] = None
        df['Longitud'] = None

        # Iterar por cada dirección
        for i, address in enumerate(df[column_name]):
            lat, lon = get_coordinates(address)
            df.at[i, 'Latitud'] = lat
            df.at[i, 'Longitud'] = lon

        # Mostrar resultado
        st.write("Resultados:")
        st.dataframe(df)

        # Permitir descarga del archivo procesado
        st.download_button(
            label="Descargar CSV con coordenadas",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name="direcciones_con_coordenadas.csv",
            mime="text/csv",
        )
