from .kupfer4 import run_kupfer_scraper
from .sodimac2 import run_sodimac_scraper
from .servimetal2 import run_servimetal_scraper
from .easy3 import run_easy_scraper
from .constructor31 import run_constructor_scraper
from .construmart2 import run_construmart_scraper

def run_all_scrapers():
    results = []
    results.append(run_kupfer_scraper())
    results.append(run_sodimac_scraper())
    results.append(run_servimetal_scraper())
    results.append(run_easy_scraper())
    results.append(run_constructor_scraper())
    results.append(run_construmart_scraper())
    return results
