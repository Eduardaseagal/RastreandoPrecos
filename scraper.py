import re
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
import time
from config import WEBDRIVER_CONFIG

def extrair_preco_bs4(url):
    headers = {
        'User-Agent': WEBDRIVER_CONFIG['user_agent']
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tentativas genéricas de encontrar o preço
        price_selectors = [
            {'class': 'price'},
            {'itemprop': 'price'},
            {'class': 'product-price'},
            {'class': 'product__price'},
            {'data-testid': 'price-value'},
            {'class': 'price__value'},
            {'class': 'productPrice'},
            {'class': 'sales-price'},
            {'class': 'current-price'},
        ]
        
        for selector in price_selectors:
            element = soup.find(attrs=selector)
            if element:
                price_text = element.get_text().strip()
                # Remove R$, símbolos e espaços, converte para float
                price = float(re.sub(r'[^\d,]', '', price_text).replace(',', '.'))
                return price
        
        # Regex para encontrar padrões de preço (R$ 1.999,99 ou 1,299.99)
        price_patterns = [
            r'R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})',
            r'\b\d{1,3}(?:,\d{3})*(?:\.\d{2})?\b'
        ]
        
        for pattern in price_patterns:
            matches = re.findall(pattern, response.text)
            if matches:
                try:
                    price = float(matches[0].replace('.', '').replace(',', '.'))
                    return price
                except ValueError:
                    continue
                    
    except Exception as e:
        print(f"Erro ao extrair preço com BeautifulSoup: {e}")
        return None
    
    return None

def extrair_preco_selenium(url):
    options = Options()
    if WEBDRIVER_CONFIG['headless']:
        options.add_argument('--headless')
    options.add_argument(f'user-agent={WEBDRIVER_CONFIG["user_agent"]}')
    
    driver = webdriver.Chrome(options=options)
    price = None
    
    try:
        driver.get(url)
        time.sleep(3)  # Espera inicial para carregamento
        
        # Tentar encontrar elementos comuns de preço
        xpaths = [
            "//*[contains(@class, 'price')]",
            "//*[@itemprop='price']",
            "//*[contains(@class, 'product-price')]",
            "//*[contains(@class, 'product__price')]",
        ]
        
        for xpath in xpaths:
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )  # PARÊNTESE FALTANTE ADICIONADO AQUI
                price_text = element.text.strip()
                price = float(re.sub(r'[^\d,.]', '', price_text).replace(',', '.'))
                break
            except:
                continue
                
    except Exception as e:
        print(f"Erro ao extrair preço com Selenium: {e}")
    finally:
        driver.quit()
    
    return price