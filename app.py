import pandas as pd
import streamlit as st

# Paso 1: Cargar el CSV en un DataFrame de pandas
ruta_csv = 'jcdcaux.csv'  # Cambia esta ruta al archivo CSV que tienes
df = pd.read_csv(ruta_csv)

# Paso 2: Preprocesamiento del DataFrame
df.fillna(0, inplace=True)
df['Zipcode'] = df['Zipcode'].astype(float).astype(int)

st.title('Búsqueda de Información')

# Bloque 1: Búsqueda por Códigos Postales
st.header("Búsqueda por Códigos Postales")
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

# Bloque 2: Búsqueda por Ciudad
st.header("Búsqueda por Ciudad")

# Crear un menú desplegable para seleccionar la ciudad
ciudades_disponibles = df['City'].unique()  # Lista de ciudades únicas en el DataFrame
ciudad_seleccionada = st.selectbox('Selecciona una ciudad', ciudades_disponibles)

# Filtrar el DataFrame por la ciudad seleccionada
df_filtrado_ciudad = df[df['City'] == ciudad_seleccionada]

# Seleccionar solo las columnas que necesitas para el resultado
df_resultado_ciudad = df_filtrado_ciudad[['Zipcode', 'Frame id', 'Full address', 'Publisher', 'City', 'Venue types']]

# Mostrar resultados del bloque de ciudades
if not df_resultado_ciudad.empty:
    st.write(f"Resultados encontrados para la ciudad: {ciudad_seleccionada}")
    st.dataframe(df_resultado_ciudad)
else:
    st.write("No se encontraron resultados para la ciudad seleccionada.")
