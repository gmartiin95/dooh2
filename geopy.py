
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import Search

st.title('Búsqueda de Información DOOH')

# Permitir al usuario cargar el archivo CSV
uploaded_file = st.file_uploader("Cargar archivo CSV", type=['csv'])

if uploaded_file is not None:
    # Cargar el CSV en un DataFrame de pandas
    df = pd.read_csv(uploaded_file)

    # Convertir Latitude y Longitude a números, ignorando valores no válidos
    df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
    df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')

    # Eliminar filas con coordenadas inválidas
    df = df.dropna(subset=['Latitude', 'Longitude'])

    # Preprocesamiento del DataFrame
    df.fillna(0, inplace=True)
    df['Zipcode'] = df['Zipcode'].astype(float).astype(int)

    # Bloque 1: Filtro por Ciudad (con multiselección)
    st.header("Filtro por Ciudad")
    ciudades_disponibles = df['City'].unique()
    ciudades_seleccionadas = st.multiselect("Selecciona una o varias ciudades", ciudades_disponibles)

    # Filtrar venue types disponibles en función de las ciudades seleccionadas
    if ciudades_seleccionadas:
        df_filtrado_por_ciudad = df[df['City'].isin(ciudades_seleccionadas)]
        venuetypes_disponibles = df_filtrado_por_ciudad['Venue types'].unique()
    else:
        venuetypes_disponibles = df['Venue types'].unique()

    # Bloque 2: Filtro por Venue type
    st.header("Filtro por Venue types")
    venuetypes_seleccionados = st.multiselect(
        "Selecciona uno o varios Venue types. Outdoor= exterior, subway=estaciones de tren, parking/garages y malls= Centros Comerciales",
        venuetypes_disponibles
    )

    # Bloque 3: Filtro por Código Postal
    st.header("Filtro por Código Postal")
    zipcodes_input = st.text_input("Ingresa códigos postales (separados por comas)")
    
    if zipcodes_input:
        zipcodes_a_buscar = [int(zip.strip()) for zip in zipcodes_input.split(',') if zip.strip().isdigit()]
    else:
        zipcodes_a_buscar = []

    # Filtrar el DataFrame en función de todos los filtros seleccionados
    df_filtrado_final = df.copy()

    # Aplicar filtros
    if ciudades_seleccionadas:
        df_filtrado_final = df_filtrado_final[df_filtrado_final['City'].isin(ciudades_seleccionadas)]
    
    if venuetypes_seleccionados:
        df_filtrado_final = df_filtrado_final[df_filtrado_final['Venue types'].isin(venuetypes_seleccionados)]
    
    if zipcodes_a_buscar:
        df_filtrado_final = df_filtrado_final[df_filtrado_final['Zipcode'].isin(zipcodes_a_buscar)]

    # Seleccionar columnas para el resultado
    df_resultado = df_filtrado_final[['Zipcode', 'Frame id', 'Full address', 'Publisher', 'City', 'Venue types', 'Latitude', 'Longitude']]

    # Mostrar resultados
    if not df_resultado.empty:
        st.write("Resultados encontrados:")
        st.dataframe(df_resultado)

        # Crear mapa interactivo
        st.header("Mapa de Ubicaciones")
        centro_mapa = [df_resultado['Latitude'].mean(), df_resultado['Longitude'].mean()]
        mapa = folium.Map(location=centro_mapa, zoom_start=12)
        
        # Crear grupo de marcadores
        marker_group = folium.FeatureGroup(name="Marcadores")
        mapa.add_child(marker_group)

        # Agregar marcadores
        for _, row in df_resultado.iterrows():
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=f"{row['Full address']} - {row['Venue types']}",
                tooltip=row['City']
            ).add_to(marker_group)

        # Agregar buscador
        search = Search(
            layer=marker_group,
            search_label='City',
            placeholder='Buscar ciudad...',
            collapsed=True
        ).add_to(mapa)

        # Mostrar mapa
        st_folium(mapa, width=700, height=500)

        # Guardar y permitir descarga del mapa
        mapa.save("mapa_interactivo.html")
        with open("mapa_interactivo.html", "rb") as file:
            btn = st.download_button(
                label="Descargar Mapa (HTML)",
                data=file,
                file_name="mapa_interactivo.html",
                mime="text/html"
            )
    else:
        st.write("No se encontraron resultados con los filtros aplicados.")
else:
    st.write("Por favor, carga un archivo CSV para comenzar.")



