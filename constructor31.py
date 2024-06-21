# scraper_app/scrapers/constructor31.py

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from scrapper_app.models import ScrapedData

data =[]

def close_popup(driver):
    try:
        popup_button = WebDriverWait(driver, 2).until(
            ec.visibility_of_element_located((By.XPATH, '//button[@class="needsclick klaviyo-close-form kl-private-reset-css-Xuajs1"]'))
        )
        popup_button.click()
    except TimeoutException:
        pass

def run_constructor_scraper():
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

    urls = [
        'https://www.constructor-31.com/perfiles-de-acero',
        'https://www.constructor-31.com/metalcon',
        'https://www.constructor-31.com/cementos-y-morteros/cementos',
        'https://www.constructor-31.com/tableros/osb',
        'https://www.constructor-31.com/soldadoras-y-complementos',
        'https://www.constructor-31.com/planchas-de-fierro'
    ]

    for url in urls:
        driver.get(url)
        sleep(2)
        driver.refresh()
        sleep(2)

        while True:
            try:
                close_popup(driver)
                boton_siguiente = driver.find_element(By.XPATH, '//a[@class="vtex-button bw1 ba fw5 v-mid relative pa0 lh-solid br2 min-h-small t-action--small bg-action-primary b--action-primary c-on-action-primary hover-bg-action-primary hover-b--action-primary hover-c-on-action-primary pointer inline-flex items-center no-underline "]')
                boton_siguiente.click()
                sleep(2)
            except:
                break

        productos = driver.find_elements(By.XPATH, '//section[@class="vtex-product-summary-2-x-container vtex-product-summary-2-x-container--vitrinaBulonferCategorias vtex-product-summary-2-x-containerNormal vtex-product-summary-2-x-containerNormal--vitrinaBulonferCategorias overflow-hidden br3 h-100 w-100 flex flex-column justify-between center tc"]')
        for producto in productos:
            titulo = producto.find_element(By.XPATH, './/span[@class="vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-productBrand--nombreProducto vtex-product-summary-2-x-brandName vtex-product-summary-2-x-brandName--nombreProducto t-body"]').text.replace(',', '.')
            precios = producto.find_elements(By.XPATH, './/span[@class="vtex-product-price-1-x-sellingPriceValue vtex-product-price-1-x-sellingPriceValue--preciobulonfer"]/span')
            texto_precio = [precio.text for precio in precios][0]
            data.append(ScrapedData.objects.create(source="Constructor31", product_name=titulo, price=texto_precio))

    driver.quit()
    print("Running constructor scraper")
    return {"scraper": "constructor", "status": "success", "data": data }
