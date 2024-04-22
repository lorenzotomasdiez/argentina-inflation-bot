import re
import datetime as dt
from bs4 import BeautifulSoup
from services.db.prices.index import get_prices
from services.db.products_markets.index import get_all_products_markets
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from selenium.common.exceptions import TimeoutException # type: ignore
from config import SELENIUM_HOST, SELENIUM_PORT, table


index_error = []
"""
- Take a product name and a URL, and return the price of the product.
:param product_name: The name of the product
:param product_url: The URL of the product
:param portion: the amount of the product you want to buy, defaults to 1 (optional)
:return: the value of the variable "list"
"""
def kilo(id, page, list, portion=1):
    product_info_container = page.find_all("div", id="productInfoContainer")
    disponibility = product_info_container[0].find_all(
        "div", class_="product_not_available"
    )

    if disponibility:
        list.update({id: 0})
        #SHOULD SAVE ERROR ON DB
        print(f"SCRAPPING_SERVICE - cotto.py - kilo: {id} not available, {list[id]}")
        return None

    try:
        # search inside product_info_container the span with the class unit
        value = product_info_container[0].find_all("span", class_="unit")[0].get_text()
    except IndexError:
        list.update({id: 0})
        index_error.append(id)
        print(f"SCRAPPING_SERVICE - cotto.py - kilo: {id} IndexError, {list[id]}")
        return None

    match = re.search(r"\$([\d,.]+)", value)

    if match:
        number = float(match.group(1).replace(".", "").replace(",", "."))
        list.update({id: number * portion})
    else:
        list.update({id: 0})
        print(f"SCRAPPING_SERVICE - cotto.py - kilo: {id} not found, {list[id]}")

"""
- Take a product name and a URL, and return the price of the product.
:param product_name: The name of the product
:param product_url: The URL of the product
:return: the value of the variable "list"
"""
def unit(id, page, list):
    product_info_container = page.find_all("div", id="productInfoContainer")
    disponibility = product_info_container[0].find_all(
        "div", class_="product_not_available"
    )

    if disponibility:
        list.update({id: 0})
        print(f"SCRAPPING_SERVICE - cotto.py - unit: {id} not available, {list[id]}")
        return None

    try:
        value = (
            product_info_container[0]
            .find_all("span", class_="atg_store_newPrice")[0]
            .get_text()
        )
    except IndexError:
        list.update({id: 0})
        index_error.append(id)
        print(f"SCRAPPING_SERVICE - cotto.py - unit: {id} IndexError, {list[id]}")
        return None

    match = re.search(r"\$([\d,.]+)", value)

    if match:
        number = float(match.group(1).replace(".", "").replace(",", "."))
        list.update({id: number})

    else:
        list.update({id: 0})
        print(f"SCRAPPING_SERVICE - cotto.py - unit: {id} not found, {list[id]}")

def scrap_cotto():
    result = {
        "date": dt.datetime.now().strftime("%Y-%m-%d")
    }
    date = result["date"]
    already_exists = get_prices(date)
    if already_exists:
        return {"error": "data already exists for this date"}

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
        if product["product_type"] == "kilo":
            if status() == True:
                driver.get(product["url"])
                driver.implicitly_wait(10)
                page = BeautifulSoup(driver.page_source, "html.parser")
                kilo(str(product["product_id"]), page, result)
            else:
                print(f"ERROR - SCRAPPING_SERVICE - cotto.py - scrap_cotto: {product['name']} no url")
        elif product["product_type"] == "unidad":
            if status() == True:
                driver.get(product["url"])
                driver.implicitly_wait(10)
                page = BeautifulSoup(driver.page_source, "html.parser")
                unit(str(product["product_id"]), page, result)
            else:
                print(f"ERROR - SCRAPPING_SERVICE - cotto.py - scrap_cotto: {product['name']} no url")
        if "nan" in result.values():
            print(f"ERROR - SCRAPPING_SERVICE - cotto.py - scrap_cotto: nan in list")
        print(f"SCRAPPING_SERVICE - cotto.py - scrap_cotto: done")

    return result
