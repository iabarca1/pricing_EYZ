# scraper_app/scrapers/construmart2.py

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from scrapper_app.models import ScrapedData
data=[]
def run_construmart_scraper():
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

    driver.get('https://www.construmart.cl/materiales-de-construccion/Perfiles-de-Acero')
    sleep(2)

    select_element = driver.find_element(By.ID, "region")
    select = Select(select_element)
    select.select_by_visible_text("XIII REGIÓN METROPOLITANA DE SANTIAGO")

    WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.ID, "tienda"))
    )

    select_element_2 = driver.find_element(By.ID, "tienda")
    select_2 = Select(select_element_2)
    select_2.select_by_visible_text("DEPARTAMENTAL")

    boton_seleccionartienda = driver.find_element(By.XPATH, '//button[@class="storeSelectorButton"]')
    boton_seleccionartienda.click()
    sleep(5)

    urls = [
        'https://www.construmart.cl/materiales-de-construccion/Perfiles-de-Acero',
        'https://www.construmart.cl/maderas-y-tableros/tableros-construccion/osb-y-cierre-perimetral',
        'https://www.construmart.cl/materiales-de-construccion/aglomerantes-y-accesorios/cementos',
        'https://www.construmart.cl/herramientas/maquinarias/soldadoras-y-complementos',
        'https://www.construmart.cl/materiales-de-construccion/fierro-y-refuerzos-para-hormigon',
        'https://www.construmart.cl/materiales-de-construccion/mallas-cercos-y-alambres/mallas-alambre-tejida'
    ]

    def hacer_scrolling_suavizado(driver, iteracion):
        bajar_hasta = 2000 * (iteracion + 1)
        inicio = (2000 * iteracion)
        for i in range(inicio, bajar_hasta, 5):
            scrolling_script = f""" window.scrollTo(0, {i})"""
            driver.execute_script(scrolling_script)
            sleep(0.01)

    for url in urls:
        driver.get(url)
        sleep(2)

        n_scrolls = 5
        for i in range(n_scrolls):
            hacer_scrolling_suavizado(driver, i)

        productos = driver.find_elements(By.XPATH, '//div[@class="vtex-search-result-3-x-galleryItem vtex-search-result-3-x-galleryItem--normal vtex-search-result-3-x-galleryItem--grid pa4"]')
        for producto in productos:
            titulo = producto.find_element(By.XPATH, './/span[@class="vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-brandName t-body"]').text.replace(',', '.')
            try:
                precios = producto.find_elements(By.XPATH, './/div[@class="pr2 flex"]//span[@class="vtex-product-price-1-x-currencyContainer vtex-product-price-1-x-currencyContainer--summary"]')
                texto_precio = [precio.text for precio in precios][0]
            except:
                texto_precio = "Sin precio"

            data.append(ScrapedData.objects.create(source="Construmart", product_name=titulo, price=texto_precio))

    driver.quit()
    print("Running construmart scraper")
    return {"scraper": "construmart", "status": "success", "data": data }

