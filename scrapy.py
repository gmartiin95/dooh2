import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import time

# Configuración de la página
st.set_page_config(page_title="Buscador de Artículos", layout="wide")

def scrape_articles_with_keywords(newspapers, keywords):
    """
    Realiza web scraping de artículos basados en palabras clave específicas.
    """
    articles = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Barra de progreso
    progress_bar = st.progress(0)
    total_newspapers = len(newspapers)
    
    for idx, (newspaper_name, base_url) in enumerate(newspapers.items()):
        try:
            st.write(f"Analizando {newspaper_name}...")
            
            response = requests.get(base_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            for link in soup.find_all('a'):
                url = link.get('href')
                title = link.get_text().strip()
                
                if url and title and any(keyword.lower() in title.lower() for keyword in keywords):
                    if not url.startswith(('http://', 'https://')):
                        url = urljoin(base_url, url)
                    
                    articles.append({
                        'newspaper': newspaper_name,
                        'title': title,
                        'url': url
                    })
            
            # Actualizar barra de progreso
            progress_bar.progress((idx + 1) / total_newspapers)
            time.sleep(1)  # Pausa para evitar sobrecarga
            
        except Exception as e:
            st.error(f"Error al analizar {newspaper_name}: {str(e)}")
    
    return pd.DataFrame(articles).drop_duplicates(subset=['url'])

# Diccionario de periódicos
spanish_newspapers = {
    'El País': 'https://www.elpais.com',
    'El Mundo': 'https://www.elmundo.es',
    'El Confidencial': 'https://www.elconfidencial.com',
    '20 Minutos': 'https://www.20minutos.es',
    'Periodista Digital': 'https://www.periodistadigital.com',
    'Huffington Post': 'https://www.huffingtonpost.es',
    'OK Diario': 'https://www.okdiario.com',
    'Público': 'https://www.publico.es',
    'El Español': 'https://www.elespanol.com',
    'elDiario.es': 'https://www.eldiario.es'
}

# Interfaz de usuario
st.title("🔍 Buscador de Artículos en Prensa")

# Área para introducir palabras clave
st.subheader("Introduce las palabras clave")
keywords_input = st.text_area(
    "Escribe las palabras clave separadas por comas",
    help="Ejemplo: alopecia, capilar, calvicie"
)

if st.button("Buscar Artículos"):
    if keywords_input:
        # Convertir el input en lista de palabras clave
        keywords = [k.strip() for k in keywords_input.split(',')]
        
        with st.spinner('Buscando artículos...'):
            # Realizar la búsqueda
            results = scrape_articles_with_keywords(spanish_newspapers, keywords)
            
            # Mostrar resultados
            if not results.empty:
                st.success(f"¡Se encontraron {len(results)} artículos!")
                
                # Mostrar resultados en una tabla
                st.dataframe(
                    results,
                    column_config={
                        "url": st.column_config.LinkColumn("URL"),
                        "title": st.column_config.TextColumn("Título"),
                        "newspaper": st.column_config.TextColumn("Periódico")
                    },
                    hide_index=True
                )
                
                # Botón para descargar resultados
                csv = results.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "Descargar resultados (CSV)",
                    csv,
                    "articulos.csv",
                    "text/csv",
                    key='download-csv'
                )
            else:
                st.warning("No se encontraron artículos con las palabras clave especificadas.")
    else:
        st.error("Por favor, introduce al menos una palabra clave.")

# Mostrar información adicional
with st.expander("ℹ️ Información sobre la aplicación"):
    st.markdown("""
    Esta aplicación realiza búsquedas en tiempo real en los principales periódicos españoles.
    
    **Características:**
    - Búsqueda simultánea en múltiples fuentes
    - Resultados en formato tabular con enlaces directos
    - Exportación de resultados a CSV
    
    **Nota:** La búsqueda puede tardar unos minutos dependiendo del número de fuentes y palabras clave.
    """)
