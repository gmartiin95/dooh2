
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium

# Paso 1: Cargar el CSV en un DataFrame de pandas
ruta_csv = 'DOOH UPDATE - Hoja 1 (1).csv'  # Cambia esta ruta si es necesario
df = pd.read_csv(ruta_csv)

# Convertir Latitude y Longitude a números, ignorando valores no válidos
df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')

# Eliminar filas con coordenadas inválidas
df = df.dropna(subset=['Latitude', 'Longitude'])

# Renombrar columnas para evitar espacios
df.rename(columns={'Venue types': 'VenueTypes'}, inplace=True)

# Convertir Zipcode a numérico y luego a entero, gestionando errores
df['Zipcode'] = pd.to_numeric(df['Zipcode'], errors='coerce').fillna(0).astype(int)

# Llenar otros valores nulos con 0
df.fillna(0, inplace=True)

st.title('Búsqueda de Información DOOH')

# ---------------- Filtro por Ciudad ----------------
st.header("Filtro por Ciudad")
ciudades_disponibles = df['City'].unique()
ciudades_seleccionadas = st.multiselect("Selecciona una o varias ciudades", ciudades_disponibles)

# Filtrar venue types según las ciudades seleccionadas
if ciudades_seleccionadas:
    df_filtrado_por_ciudad = df[df['City'].isin(ciudades_seleccionadas)]
    venuetypes_disponibles = df_filtrado_por_ciudad['VenueTypes'].unique()
else:
    venuetypes_disponibles = df['VenueTypes'].unique()

# ---------------- Filtro por Venue Types ----------------
st.header("Filtro por VenueTypes")
venuetypes_seleccionados = st.multiselect(
    "Selecciona uno o varios Venue types. Outdoor = exterior, subway = estaciones de tren, parking/garages y malls = Centros Comerciales",
    venuetypes_disponibles
)

# ---------------- Filtrado final ----------------
df_filtrado_final = df.copy()

if ciudades_seleccionadas:
    df_filtrado_final = df_filtrado_final[df_filtrado_final['City'].isin(ciudades_seleccionadas)]

if venuetypes_seleccionados:
    df_filtrado_final = df_filtrado_final[df_filtrado_final['VenueTypes'].isin(venuetypes_seleccionados)]

# Selección de columnas para mostrar
columnas_a_mostrar = ['Zipcode', 'Frame id', 'Full address', 'Publisher', 'City', 'VenueTypes', 'Latitude', 'Longitude']
df_resultado = df_filtrado_final[columnas_a_mostrar]

if not df_resultado.empty:
    st.write("Resultados encontrados con los filtros aplicados:")
    st.dataframe(df_resultado)

    # ---------------- Mapa con resultados ----------------
    st.header("Mapa de ubicaciones filtradas")
    m = folium.Map(location=[df_resultado['Latitude'].mean(), df_resultado['Longitude'].mean()], zoom_start=11)
    for _, row in df_resultado.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=row['Full address']
        ).add_to(m)
    st_folium(m, width=700, height=500)

# ---------------- Búsqueda por Códigos Postales ----------------
st.header("Búsqueda por Códigos Postales (No aplicable filtros de Ciudad y Venue)")
st.write("Ingresa los códigos postales separados por comas (Ejemplo: 4006, 4004, 37004)")

input_zipcodes = st.text_input('Códigos postales', '4006, 4004, 37004')

try:
    zipcodes_a_buscar = [int(zipcode.strip()) for zipcode in input_zipcodes.split(',') if zipcode.strip().isdigit()]
    df_filtrado_zip = df[df['Zipcode'].isin(zipcodes_a_buscar)]
    df_resultado_zip = df_filtrado_zip[['Zipcode', 'Frame id', 'Full address', 'Publisher', 'City', 'VenueTypes']]

    if not df_resultado_zip.empty:
        st.write("Resultados encontrados por códigos postales:")
        st.dataframe(df_resultado_zip)
    else:
        st.write("No se encontraron resultados para los códigos postales ingresados.")
except ValueError:
    st.error("Por favor, ingresa solo números separados por comas como códigos postales.")
