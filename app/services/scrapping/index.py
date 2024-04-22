from .cotto import scrap_cotto
from config import basket_csv
from services.db.prices.index import add_prices

def scrapping_test():
    return "scrapping test"

def scrap():
    coto_results = scrap_cotto()
    if "error" in coto_results:
        return coto_results
    else:
        prices_results = add_prices(prices = coto_results, market_id = 1)
        return prices_results
