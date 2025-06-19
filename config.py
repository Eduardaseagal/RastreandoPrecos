import os
from pathlib import Path

# Configurações de diretório
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "produtos.db"

# Configurações de e-mail (preencher com seus dados)
EMAIL_CONFIG = {
    'sender': 'email@gmail.com - usuario',
    'password': 'Senha do app é melhor e mais seguro',  # Ou senha de app se usar Gmail
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587
}

# Configurações do navegador para Selenium
WEBDRIVER_CONFIG = {
    'headless': True,
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}