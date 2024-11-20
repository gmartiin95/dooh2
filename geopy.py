pip install streamlit geopy pandas

import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

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



