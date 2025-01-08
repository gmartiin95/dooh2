import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import time
from datetime import datetime, timedelta
import re

# Función de scraping
def scrape_health_articles(newspapers, health_keywords, max_age_days=30):
    """
    Realiza web scraping de artículos relacionados con salud en periódicos españoles.
    
    Args:
        newspapers (dict): Diccionario con los periódicos y sus URLs base
        health_keywords (list): Lista de palabras clave para buscar en los títulos
        max_age_days (int): Máximo número de días de antigüedad permitidos para los artículos
        
    Returns:
        DataFrame: URLs y títulos de artículos relacionados con salud
    """
    
    # Lista para almacenar los resultados
    health_articles = []
    
    # Headers para simular un navegador
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Fecha límite para filtrar artículos
    cutoff_date = datetime.now() - timedelta(days=max_age_days)
    
    # Patrones comunes de fechas en URLs españolas
    date_patterns = [
        r'/(\d{4})/(\d{2})/(\d{2})/',  # formato /2024/01/08/
        r'/(\d{4})-(\d{2})-(\d{2})/',  # formato /2024-01-08/
        r'/(\d{2})-(\d{2})-(\d{4})/',  # formato /08-01-2024/
        r'/(\d{8})/'                    # formato /20240108/
    ]
    
    # Mostrar un mensaje general de "Analizando periódicos"
    st.write("Analizando periódicos...")
    
    for newspaper_name, base_url in newspapers.items():
        try:
            response = requests.get(base_url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            for link in soup.find_all('a'):
                url = link.get('href')
                title = link.get_text().strip()
                
                if url and title and any(keyword in title.lower() for keyword in health_keywords):
                    # Convertir URLs relativas a absolutas
                    if not url.startswith(('http://', 'https://')):
                        url = urljoin(base_url, url)
                    
                    # Intentar extraer la fecha del artículo
                    article_date = None
                    
                    # Buscar fecha en la URL
                    for pattern in date_patterns:
                        match = re.search(pattern, url)
                        if match:
                            try:
                                # Asegurarnos de que estamos trabajando con cadenas
                                date_str = str(match.group(1))  # Convertir el valor a cadena
                                if len(date_str) == 8:  # Si encontramos fecha en formato /20240108/
                                    article_date = datetime.strptime(date_str, '%Y%m%d')
                                else:
                                    # Reordenar los grupos según el patrón
                                    date_parts = [int(g) for g in match.groups()]
                                    if len(str(date_parts[0])) == 4:  # Comprobar si el primer número es el año
                                        article_date = datetime(date_parts[0], date_parts[1], date_parts[2])
                                    else:  # Si el último número es el año
                                        article_date = datetime(date_parts[2], date_parts[1], date_parts[0])
                            except ValueError:
                                continue
                    
                    # Si no podemos determinar la fecha o el artículo es reciente, lo incluimos
                    if article_date is None or article_date >= cutoff_date:
                        health_articles.append({
                            'newspaper': newspaper_name,
                            'title': title,
                            'url': url,
                            'fecha': article_date
                        })
            
            time.sleep(2)  # Esperar 2 segundos entre cada periódico
            
        except Exception as e:
            st.error(f"Error al analizar {newspaper_name}: {str(e)}")
    
    # Crear DataFrame con los resultados
    df = pd.DataFrame(health_articles)
    
    # Eliminar duplicados
    df = df.drop_duplicates(subset=['url'])
    
    return df

# Configuración de la aplicación Streamlit
st.title("Scraping de Artículos sobre Inteligencia Artificial en Periódicos Españoles")

# Campo para introducir palabras clave
user_keywords = st.text_input(
    "Introduce palabras clave separadas por comas (por ejemplo: inteligencia artificial, machine learning, IA):",
    "inteligencia artificial, machine learning, IA, ChatGPT, OpenAI, Claude, aprendizaje automático, deep learning, redes neuronales, algoritmos, ciencia de datos, automatización, modelos generativos"
)

# Convertir las palabras clave en una lista
health_keywords = [keyword.strip().lower() for keyword in user_keywords.split(",")]

# Botón para iniciar el scraping
if st.button("Buscar artículos"):
    # Definir los periódicos a analizar
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
        'elDiario.es': 'https://www.eldiario.es',
        'El Confidencial Digital': 'https://www.elconfidencialdigital.com',
        'La Información': 'https://www.lainformacion.com',
        'Europa Press': 'https://www.europapress.es',
        'Diario Información': 'https://www.diarioinformacion.com',
        'ESdiario': 'https://www.esdiario.com',
        'La Gaceta': 'https://www.gaceta.es',
        'El Plural': 'https://www.elplural.com',
        'Nueva Tribuna': 'https://www.nuevatribuna.es',
        'InfoLibre': 'https://www.infolibre.es',
        'AS': 'https://www.as.com',
        'Marca': 'https://www.marca.com',
        'Sport': 'https://www.sport.es',
        'Kiosko': 'https://www.kiosko.net',
        'Columna Cero': 'https://www.columnacero.com',
        'Vozpópuli': 'https://www.vozpopuli.com',
        'Libertad Digital': 'https://www.libertaddigital.com',
        'El Independiente': 'https://www.elindependiente.com',
        'La Razón': 'https://www.larazon.es',
        'The Objective': 'https://www.theobjective.com',
        'Expansión': 'https://expansion.com',
        'El Economista': 'https://eleconomista.es',
        'Libre Mercado': 'https://libremercado.com',
        'Cinco Días': 'https://cincodias.elpais.com',
        'El Blog Salmón': 'https://elblogsalmon.com',
        'El Confidencial (Mercados)': 'https://elconfidencial.com/mercados',
        'El Boletín': 'https://elboletin.com',
        'Acciones de Bolsa': 'https://accionesdebolsa.com',
        'Gestiopolis': 'https://gestiopolis.com',
        'Pymes y Autónomos': 'https://pymesyautonomos.com',
        'Autónomos y Emprendedor': 'https://autonomosyemprendedor.es',
        'Emprendedores': 'https://emprendedores.es',
        'Economía Digital': 'https://economiadigital.es',
        'Bolsamanía': 'https://bolsamania.com',
        'Business Insider España': 'https://businessinsider.es',
        'InfoBolsa': 'https://infobolsa.es',
        'PC Bolsa': 'https://pcbolsa.com',
        'Intereconomía': 'https://intereconomia.com',
        'El Referente': 'https://elreferente.es',
        'Negocios y Emprendimiento': 'https://negociosyemprendimiento.org',
        'Libertad Digital': 'https://libertaddigital.com',
        'El Mundo (Economía)': 'https://elmundo.es/economia.html',
        'El Español (Invertia)': 'https://elespanol.com/invertia',
        'La Vanguardia (Economía)': 'https://lavanguardia.com/economia',
        'Merca2': 'https://merca2.es',
        'El Confidencial (Mercados)': 'https://elconfidencial.com/mercados',
        'Empresite (El Economista)': 'https://empresite.eleconomista.es',
        'Cosmopolitan': 'https://cosmopolitan.com',
        'Hola': 'https://hola.com',
        'Women\'s Health': 'https://womenshealthmag.com',
        'Yo Dona (El Mundo)': 'https://elmundo.es/yodona.html',
        'Divinity': 'https://divinity.es',
        'Marie Claire': 'https://marie-claire.es',
        'Elle': 'https://elle.com',
        'Lecturas': 'https://lecturas.com',
        'Diez Minutos': 'https://diezminutos.es',
        'Mujer Hoy': 'https://mujerhoy.com',
        'Nueva Mujer': 'https://nuevamujer.com',
        'Clara': 'https://clara.es',
        'Telva': 'https://telva.com',
        'Style Lovely': 'https://stylelovely.com',
        'Fashion United': 'https://fashionunited.es',
        'Vanitatis (El Confidencial)': 'https://vanitatis.elconfidencial.com',
        'Fashion Network (España)': 'https://es.fashionnetwork.com',
        'Modaes': 'https://modaes.com'
    }
    
    # Ejecutar el scraping
    results = scrape_health_articles(spanish_newspapers, health_keywords)
    
    # Mostrar resultados en una tabla
    if not results.empty:
        st.write(f"Se encontraron {len(results)} artículos relacionados con las palabras clave:")
        st.dataframe(results)
        
        # Opción para descargar los resultados en CSV
        st.download_button(
            label="Descargar resultados en CSV",
            data=results.to_csv(index=False).encode('utf-8'),
            file_name='articulos_salud.csv',
            mime='text/csv'
        )
    else:
        st.warning("No se encontraron artículos relacionados con las palabras clave proporcionadas.")
