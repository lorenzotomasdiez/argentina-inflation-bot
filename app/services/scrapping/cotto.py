import re
from bs4 import BeautifulSoup
from services.db.prices.index import get_prices
from services.db.products_markets.index import get_all_products_markets
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from selenium.common.exceptions import TimeoutException # type: ignore
from config import SELENIUM_HOST, SELENIUM_PORT, get_date_now


index_error = []
"""
- Take a product name and a URL, and return the price of the product.
:param product_name: The name of the product
:param product_url: The URL of the product
:param portion: the amount of the product you want to buy, defaults to 1 (optional)
:return: the value of the variable "list"
"""
def kg(product, page, result):
    id = str(product["product_id"])
    quantity = product["quantity"]
    product_info_container = page.find_all("div", id="productInfoContainer")
    disponibility = product_info_container[0].find_all(
        "div", class_="product_not_available"
    )

    if disponibility:
        result.update({id: 0})
        #SHOULD SAVE ERROR ON DB
        print(f"SCRAPPING_SERVICE - cotto.py - kilo: {id} not available, {result[id]}")
        return None

    try:
        # search inside product_info_container the span with the class unit
        value = product_info_container[0].find_all("span", class_="unit")[0].get_text()
    except IndexError:
        result.update({id: 0})
        index_error.append(id)
        print(f"SCRAPPING_SERVICE - cotto.py - kilo: {id} IndexError, {result[id]}")
        return None

    match = re.search(r"\$([\d,.]+)", value)

    if match:
        number = float(match.group(1).replace(".", "").replace(",", "."))
        result.update({id: number * quantity})
    else:
        result.update({id: 0})
        print(f"SCRAPPING_SERVICE - cotto.py - kilo: {id} not found, {result[id]}")

"""
- Take a product name and a URL, and return the price of the product.
:param product_name: The name of the product
:param product_url: The URL of the product
:return: the value of the variable "list"
"""
def unit(product, page, result):
    id = str(product["product_id"])
    quantity = product["quantity"]
    product_info_container = page.find_all("div", id="productInfoContainer")
    disponibility = product_info_container[0].find_all(
        "div", class_="product_not_available"
    )

    if disponibility:
        result.update({id: 0})
        print(f"SCRAPPING_SERVICE - cotto.py - unit: {id} not available, {result[id]}")
        return None

    try:
        value = (
            product_info_container[0]
            .find_all("span", class_="atg_store_newPrice")[0]
            .get_text()
        )
    except IndexError:
        result.update({id: 0})
        index_error.append(id)
        print(f"SCRAPPING_SERVICE - cotto.py - unit: {id} IndexError, {result[id]}")
        return None

    match = re.search(r"\$([\d,.]+)", value)

    if match:
        number = float(match.group(1).replace(".", "").replace(",", "."))
        result.update({id: number / quantity})

    else:
        result.update({id: 0})
        print(f"SCRAPPING_SERVICE - cotto.py - unit: {id} not found, {result[id]}")

def scrap_cotto():
    result = {
        "date": get_date_now()
    }
    date = result["date"]

    already_exists = get_prices(date, market_id=1)
    if len(already_exists) > 0:
        return {"error": f"Prices for date {date} already exist in the database"}

    # should fetch coto id from db
    products = get_all_products_markets(1)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")

    driver = webdriver.Remote(f"{SELENIUM_HOST}:{SELENIUM_PORT}/wd/hub", options=chrome_options)

    def status():
        try:
            status = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            return True
        except TimeoutException:
            print(f"SCRAPPING_SERVICE - cotto.py - scrap_cotto: TimeoutException")
            driver.quit()
            return None

    for product in products:
        if product["measurement"] == "kg" or product["measurement"] == "l":
            if status() == True:
                driver.get(product["url"])
                driver.implicitly_wait(10)
                page = BeautifulSoup(driver.page_source, "html.parser")
                kg(product, page, result)
            else:
                print(f"ERROR - SCRAPPING_SERVICE - cotto.py - scrap_cotto: {product['name']} no url")
        elif product["measurement"] == "unit":
            if status() == True:
                driver.get(product["url"])
                driver.implicitly_wait(10)
                page = BeautifulSoup(driver.page_source, "html.parser")
                unit(product, page, result)
            else:
                print(f"ERROR - SCRAPPING_SERVICE - cotto.py - scrap_cotto: {product['name']} no url")
        if "nan" in result.values():
            print(f"ERROR - SCRAPPING_SERVICE - cotto.py - scrap_cotto: nan in list")
        print(f"SCRAPPING_SERVICE - cotto.py - scrap_cotto: done")

    return result
