import pandas as pd
import streamlit as st

# Paso 1: Cargar el CSV en un DataFrame de pandas
ruta_csv = 'jcdcaux.csv'  # Cambia esta ruta al archivo CSV que tienes
df = pd.read_csv(ruta_csv)

# Paso 2: Preprocesamiento del DataFrame
df.fillna(0, inplace=True)
df['Zipcode'] = df['Zipcode'].astype(float).astype(int)

st.title('Búsqueda de Información')
# Bloque 2: Búsqueda por Ciudad (Elección Múltiple)
st.header("Búsqueda por Ciudad")

# Crear un campo de selección múltiple para las ciudades
ciudades_disponibles = df['City'].unique()  # Lista de ciudades únicas en el DataFrame
ciudades_seleccionadas = st.multiselect('Selecciona una o varias ciudades', ciudades_disponibles)

# Filtrar el DataFrame por las ciudades seleccionadas (si hay alguna seleccionada)
if ciudades_seleccionadas:
    df_filtrado_ciudad = df[df['City'].isin(ciudades_seleccionadas)]
    df_resultado_ciudad = df_filtrado_ciudad[['Zipcode', 'Frame id', 'Full address', 'Publisher', 'City', 'Venue types']]

    # Mostrar resultados del bloque de ciudades
    if not df_resultado_ciudad.empty:
        st.write(f"Resultados encontrados para las ciudades seleccionadas:")
        st.dataframe(df_resultado_ciudad)
    else:
        st.write("No se encontraron resultados para las ciudades seleccionadas.")
else:
    st.write("Por favor, selecciona al menos una ciudad.")
    
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
# Bloque 3: Búsqueda por venue_type (Elección Múltiple)
st.header("Búsqueda por Venue type")

# Crear un campo de selección múltiple para las ciudades
tipo_disponibles = df['Venue type'].unique()  # Lista de ciudades únicas en el DataFrame
tipos_seleccionadas = st.multiselect('Selecciona una o varios Venues', tipo_disponibles)

# Filtrar el DataFrame por las ciudades seleccionadas (si hay alguna seleccionada)
if tipos_seleccionadas:
    df_filtrado_tipo= df[df['Venue type'].isin(tipos_seleccionadas)]
    df_resultado_tipo = df_filtrado_tipo[['Zipcode', 'Frame id', 'Full address', 'Publisher', 'City', 'Venue types']]

    # Mostrar resultados del bloque de ciudades
    if not df_resultado_tipo.empty:
        st.write(f"Resultados encontrados para los Venues seleccionados:")
        st.dataframe(df_resultado_tipo)
    else:
        st.write("No se encontraron resultados para los Venues seleccionadas.")
else:
    st.write("Por favor, selecciona al menos un Venue.")
