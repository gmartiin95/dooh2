import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import time

def scrape_health_articles(newspapers, keywords):
    """
    Realiza web scraping de artículos basado en palabras clave proporcionadas
    """
    health_articles = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Barra de progreso de Streamlit
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, (newspaper_name, base_url) in enumerate(newspapers.items()):
        try:
            status_text.text(f"Analizando {newspaper_name}...")
            
            response = requests.get(base_url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            for link in soup.find_all('a'):
                url = link.get('href')
                title = link.get_text().strip()
                
                if url and title and any(keyword.lower() in title.lower() for keyword in keywords):
                    if not url.startswith(('http://', 'https://')):
                        url = urljoin(base_url, url)
                    
                    health_articles.append({
                        'newspaper': newspaper_name,
                        'title': title,
                        'url': url
                    })
            
            # Actualizar barra de progreso
            progress_bar.progress((idx + 1) / len(newspapers))
            time.sleep(1)
            
        except Exception as e:
            st.error(f"Error al analizar {newspaper_name}: {str(e)}")
    
    progress_bar.empty()
    status_text.empty()
    
    return pd.DataFrame(health_articles).drop_duplicates(subset=['url'])

def main():
    st.title("🔍 Buscador de Artículos de Salud")
    st.markdown("### Encuentra artículos relacionados con la salud en los principales periódicos españoles")
    
    # Diccionario de periódicos
    spanish_newspapers = {
        'El País': 'https://elpais.com',
        'El Mundo': 'https://www.elmundo.es',
        'ABC': 'https://www.abc.es',
        'La Vanguardia': 'https://www.lavanguardia.com',
        '20 Minutos': 'https://www.20minutos.es'
    }
    
    # Input para palabras clave
    st.markdown("#### Introduce las palabras clave")
    st.markdown("*Escribe una palabra y presiona Enter para añadirla*")
    keywords_input = st.text_area("", placeholder="Ejemplo: salud, medicina, hospital...")
    
    if keywords_input:
        # Convertir el texto en lista de palabras clave
        keywords = [keyword.strip() for keyword in keywords_input.split('\n') if keyword.strip()]
        
        # Mostrar palabras clave actuales
        st.markdown("#### Palabras clave seleccionadas:")
        st.write(', '.join(keywords))
        
        # Botón para iniciar el scraping
        if st.button("🚀 Buscar Artículos"):
            with st.spinner('Buscando artículos...'):
                results = scrape_health_articles(spanish_newspapers, keywords)
                
                if not results.empty:
                    st.success(f"¡Se encontraron {len(results)} artículos!")
                    
                    # Mostrar resultados en una tabla
                    st.markdown("### Resultados encontrados")
                    st.dataframe(results)
                    
                    # Botón para descargar resultados
                    csv = results.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Descargar resultados como CSV",
                        data=csv,
                        file_name="articulos_encontrados.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("No se encontraron artículos con las palabras clave proporcionadas.")
    
    # Información adicional
    with st.expander("ℹ️ Información sobre la herramienta"):
        st.markdown("""
        - Esta herramienta busca artículos en los principales periódicos españoles
        - Puedes introducir múltiples palabras clave separadas por Enter
        - Los resultados incluyen el título del artículo y su URL
        - Puedes descargar los resultados en formato CSV
        """)

if __name__ == "__main__":
    main()
