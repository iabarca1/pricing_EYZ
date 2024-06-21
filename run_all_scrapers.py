from kupfer4 import run_kupfer_scraper
from constructor31 import run_constructor31_scraper
from construmart2 import run_construmart_scraper
from easy3 import run_easy_scraper
from servimetal2 import run_servimetal_scraper
from sodimac2 import run_sodimac_scraper

def execute():
    datos = {
        "Kupfer": run_kupfer_scraper(),
        "Constructor 31": run_constructor31_scraper(),
        "Construmart": run_construmart_scraper(),
        "Easy": run_easy_scraper(),
        "Servimetal": run_servimetal_scraper(),
        "Sodimac": run_sodimac_scraper(),
    }
    return datos
