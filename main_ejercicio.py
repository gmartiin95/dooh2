# CALIDAD DEL AIRE EN MADRID

# Importaciones
import streamlit as st
import funct_ejercicio as ft

# Configuración de la página
ft.config_page()

# Cargar los datos
path = 'air_quality_madrid.csv'
df = ft.cargar_datos(path)

# 3. MENÚ
menu = st.sidebar.selectbox('Selecciona una opción', 
                    ['Home', 'Datos', 'Filtros'])

if menu == 'Home':
    if df.columns[0] == 'Unnamed: 0':
        df = df.drop(columns='Unnamed: 0')
    ft.home(df)
elif menu == 'Datos':
    if df.columns[0] == 'Unnamed: 0':
        df = df.drop(columns='Unnamed: 0')
    ft.data(df)
elif menu == 'Filtros':
    if df.columns[0] == 'Unnamed: 0':
        df = df.drop(columns='Unnamed: 0')
    ft.filtros(df)