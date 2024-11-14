# Paso 1: Cargar el CSV en un DataFrame de pandas
ruta_csv = 'jcdcaux-Hoja-1-_2_.csv'  # Cambia esta ruta al archivo CSV que tienes
df = pd.read_csv(ruta_csv)

# Paso 2: Preprocesamiento del DataFrame
df.fillna(0, inplace=True)
df['Zipcode'] = df['Zipcode'].astype(float).astype(int)

# Paso 3: Crear una interfaz para que el usuario ingrese los códigos postales
st.title('Búsqueda por ciudad')
st.write("Ingresa las ciudades separadas por comas")
# Caja de texto para ingresar los códigos postales
input_ciudades = st.text_input('Ciudad', 'Madrid, Barcelona')  # Valor por defecto

# Convertir los códigos postales ingresados en una lista de enteros
ciudades_a_buscar = [str(city.strip()) for city in input_ciudades.split(',')]
# Paso 4: Filtrar el DataFrame para obtener solo las filas con códigos postales que coinciden
df_filtrado_ciudad = df[df['City'].isin(ciudades_a_buscar)]

# Paso 3: Crear una interfaz para que el usuario ingrese los códigos postales
st.title('Búsqueda de Códigos Postales')
st.write("Ingresa los códigos postales separados por comas (Ejemplo: 4006, 4004, 37004)")

# Caja de texto para ingresar los códigos postales
input_zipcodes = st.text_input('Códigos postales', '4006, 4004, 37004')  # Valor por defecto

# Convertir los códigos postales ingresados en una lista de enteros
zipcodes_a_buscar = [int(zipcode.strip()) for zipcode in input_zipcodes.split(',')]

# Paso 4: Filtrar el DataFrame para obtener solo las filas con códigos postales que coinciden
df_filtrado = df[df['Zipcode'].isin(zipcodes_a_buscar)]

# Paso 5: Seleccionar solo las columnas que necesitas
df_resultado = df_filtrado[['Zipcode', 'Frame id', 'Full address', 'Publisher', 'City', 'Venue types']]

# Paso 6: Mostrar el resultado en una tabla
if not df_resultado.empty:
    st.write("Resultados encontrados:")
    st.dataframe(df_resultado)
else:
    st.write("No se encontraron resultados para los códigos postales ingresados.")


