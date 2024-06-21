from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from scrapper_app.models import ScrapedData

def run_kupfer_scraper():
    data = []

    urls = [
        'https://www.kupfer.cl/aceros/perfiles.html',
        'https://www.kupfer.cl/aceros/angulos.html',
        'https://www.kupfer.cl/aceros/planchas.html',
        'https://www.kupfer.cl/aceros/pletinas.html'
    ]

    opts = Options()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--disable-gpu')
    opts.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

    for url in urls:
        driver.get(url)
        sleep(2)

        while True:
            productos = driver.find_elements(By.XPATH, '//li[@class="item product product-item"]')
            for producto in productos:
                titulo = producto.find_element(By.XPATH, './/a[@class="product-item-link"]').text.replace(',', '.')
                try:
                    precio_oferta = producto.find_element(By.XPATH, './/span[@class="special-price"]//span[@class="price"]').text
                except NoSuchElementException:
                    precio_oferta = "No hay precio oferta"

                try:
                    precio_original = producto.find_element(By.XPATH, './/span[@class="old-price"]//span[@class="price"]').text
                except NoSuchElementException:
                    try:
                        precio_original = producto.find_element(By.XPATH, './/span[@class="price-container price-final_price tax weee"]//span[@class="price"]').text
                    except NoSuchElementException:
                        precio_original = "No disponible"

                precio = precio_oferta if precio_oferta != "No hay precio oferta" else precio_original

                data.append(ScrapedData.objects.create(source="Kupfer", product_name=titulo, price=precio))

            try:
                boton_siguiente = driver.find_element(By.XPATH, '//a[@class="action  next"]')
                boton_siguiente.click()
            except NoSuchElementException:
                break

    driver.quit()
    return {"scraper": "kupfer", "status": "success", "data": data}
