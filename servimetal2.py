# scraper_app/scrapers/servimetal2.py

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from scrapper_app.models import ScrapedData
data =[]
def run_servimetal_scraper():
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

    urls = [
        'https://servimetal.cl/categoria-producto/perfiles-cerrados/perfiles-cuadrados/',
        'https://servimetal.cl/categoria-producto/perfiles-cerrados/perfiles-rectangulares/',
        'https://servimetal.cl/categoria-producto/fierros-laminados/ngulos-laminados/',
        'https://servimetal.cl/categoria-producto/fierros-laminados/fierro-estriado-construccin/',
        'https://servimetal.cl/categoria-producto/mallas-galvanizadas/mallas-cerco-electrosoldadas/',
        'https://servimetal.cl/categoria-producto/planchas-lc-y-lf/planchas-largo-3000-mm/',
        'https://servimetal.cl/categoria-producto/insumos/soldaduras-y-mig/',
        'https://servimetal.cl/categoria-producto/fierros-laminados/pletinas/',
        'https://servimetal.cl/categoria-producto/perfiles-abiertos/angulos-doblados/',
        'https://servimetal.cl/categoria-producto/perfiles-abiertos/canales/',
        'https://servimetal.cl/categoria-producto/perfiles-abiertos/costaneras/',
        'https://servimetal.cl/categoria-producto/metalcon-y-vulcometal/estructural/'
    ]

    def procesar_productos(productos):
        for producto in productos:
            titulo = producto.find_element(By.XPATH, './td[2]/div/div[1]/a').text
            precio = producto.find_element(By.XPATH, './td[4]/div/div/span/div/span/span[2]').text
            data.append(ScrapedData.objects.create(source="Servimetal", product_name=titulo, price=precio))

    for url in urls:
        driver.get(url)
        sleep(2)

        while True:
            sleep(4)
            productos_pares = driver.find_elements(By.XPATH, '//tr[@class="wcpt-row wcpt-even wcpt-product-type-simple wcpt-row--init"]')
            productos_impares = driver.find_elements(By.XPATH, '//tr[@class="wcpt-row wcpt-odd wcpt-product-type-simple wcpt-row--init"]')
            procesar_productos(productos_pares)
            procesar_productos(productos_impares)

            try:
                boton_siguiente = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, '//a[@class="next page-numbers"]')))
                boton_siguiente.click()
            except:
                break

    driver.quit()
    print("Running servimetal scraper")
    return {"scraper": "servimetal", "status": "success", "data": data }
