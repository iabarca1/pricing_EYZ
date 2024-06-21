# scraper_app/scrapers/easy3.py

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from scrapper_app.models import ScrapedData
data=[]
def run_easy_scraper():
    urls = [
        'https://www.easy.cl/materiales-de-construccion/perfiles-de-acero-y-galvanizados',
        'https://www.easy.cl/materiales-de-construccion/cemento-morteros-y-aditivos/cementos',
        'https://www.easy.cl/herramientas/maquinaria-y-herramientas-estacionarias/maquinas-de-soldar-y-electrodos'
    ]

    def hacer_scrolling_suavizado(driver, iteracion):
        bajar_hasta = 2000 * (iteracion + 1)
        inicio = (2000 * iteracion)
        for i in range(inicio, bajar_hasta, 5):
            scrolling_script = f""" window.scrollTo(0, {i})"""
            driver.execute_script(scrolling_script)

    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

    for url in urls:
        driver.get(url)
        sleep(2)

        while True:
            n_scrolls = 0
            max_scrolls = 10
            max_productos = 40

            sleep(2)
            productos = driver.find_elements(By.XPATH, '//div[@class="easycl-search-result-0-x-galleryItem easycl-search-result-0-x-galleryItem--normal easycl-search-result-0-x-galleryItem--grid pa4"]')

            while len(productos) < max_productos and n_scrolls < max_scrolls:
                hacer_scrolling_suavizado(driver, n_scrolls)
                n_scrolls += 1
                productos = driver.find_elements(By.XPATH, '//div[@class="easycl-search-result-0-x-galleryItem easycl-search-result-0-x-galleryItem--normal easycl-search-result-0-x-galleryItem--grid pa4"]')
                sleep(2)

            for producto in productos:
                titulo = producto.find_element(By.XPATH, './/span[@class="vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-productBrand--summaryName vtex-product-summary-2-x-brandName vtex-product-summary-2-x-brandName--summaryName t-body"]').text.replace(',', '.')
                precio = producto.find_element(By.XPATH, './/div[@class="easycl-precio-cencosud-0-x-lastPrice "]').text
                data.append(ScrapedData.objects.create(source="Easy", product_name=titulo, price=precio))

            try:
                boton_siguiente = driver.find_element(By.XPATH, '//a[@class=" easycl-custom-blocks-4-x-customPagination__button easycl-custom-blocks-4-x-customPagination__buttonNext"]')
                boton_siguiente.click()
            except:
                break

    driver.quit()
    print("Running easy scraper")
    return {"scraper": "easy", "status": "success", "data": data }
