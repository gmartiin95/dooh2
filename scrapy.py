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
        'OK Diario': 'https://www.okdiario.com
