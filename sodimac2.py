# scraper_app/scrapers/sodimac2.py

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
data=[]
def run_sodimac_scraper():
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

    urls = [
        'https://sodimac.falabella.com/sodimac-cl/category/CATG10755/Perfiles',
        'https://sodimac.falabella.com/sodimac-cl/category/CATG10754/Fierro',
        'https://sodimac.falabella.com/sodimac-cl/category/CATG10753/Materiales-de-Obra-Gruesa',
        'https://sodimac.falabella.com/sodimac-cl/category/CATG10760/Planchas-OSB',
        'https://sodimac.falabella.com/sodimac-cl/category/CATG10759/Plancha-de-terciado',
        'https://sodimac.falabella.com/sodimac-cl/category/CATG10757/Cierres-Perimetrales'
    ]

    for url in urls:
        driver.get(url)
        driver.refresh()
        driver.execute_script("window.scrollBy(0, 5000)")
        WebDriverWait(driver, 20).until(ec.presence_of_all_elements_located((By.XPATH, '//div[@id="testId-searchResults-products"]')))

        while True:
            sleep(2)
            WebDriverWait(driver, 20).until(ec.presence_of_all_elements_located((By.XPATH, '//div[@id="testId-searchResults-products"]')))
            productos = driver.find_elements(By.XPATH, '//div[@id="testId-searchResults-products"]/div')
            for producto in productos:
                try:
                    titulo = producto.find_element(By.XPATH, './a/div[2]/div/b').text
                except:
                    titulo = "Sin titulo"
                try:
                    precio = producto.find_element(By.XPATH, './a/div[3]/div/ol/li/div/span').text
                except:
                    precio = "Sin precio"

                data.append(ScrapedData.objects.create(source="Sodimac", product_name=titulo.replace(',', '.'), price=precio))

            try:
                sleep(3)
                driver.refresh()
                sleep(5)
                boton_siguiente = WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.XPATH, '//div/div[2]/div[2]/button')))
                boton_siguiente.click()
                WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="testId-searchResults-products"]/div')))
            except:
                break

    driver.quit()
    print("Running sodimac scraper")
    return {"scraper": "sodimac", "status": "success", "data": data }
