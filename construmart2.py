from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def run_construmart_scraper():
    # Configuración del driver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # URL del scraper
    url = 'https://construmart.cl/products'
    driver.get(url)
    sleep(3)  # Esperar a que la página cargue

    productos = []

    # Ejemplo de cómo extraer los productos
    items = driver.find_elements(By.CLASS_NAME, 'product-item')
    for item in items:
        nombre = item.find_element(By.CLASS_NAME, 'product-title').text
        precio = item.find_element(By.CLASS_NAME, 'price').text
        productos.append({
            'nombre': nombre,
            'precio': float(precio.replace('$', '').replace('.', '').replace(',', '.'))
        })

    driver.quit()
    return productos
