from config import SELENIUM_HOST, SELENIUM_PORT
from services.db.products_markets.index import get_all_products_markets
from services.db.prices.index import get_prices
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from selenium.common.exceptions import TimeoutException # type: ignore
from config import SELENIUM_HOST, SELENIUM_PORT, get_date_now
from bs4 import BeautifulSoup

def get_price_by_kg_dia(product, result, driver, prod_url, status):
    product_name = product["name"]
    product_id = str(product["product_id"])
    product_quantity = product["quantity"]
    if status() == True:
        driver.get(prod_url)
        driver.implicitly_wait(10)
        page = BeautifulSoup(driver.page_source, "html.parser")
        container = page.find_all("div", class_="vtex-flex-layout-0-x-flexRowContent--product-unit")
        try:
            price_str = container[0].find_all("span", class_="vtex-product-specifications-1-x-specificationValue")[0].get_text()
        except IndexError:
            result.update({product_id: 0})
            print(f"SCRAPPING_SERVICE - dia.py - get_price_by_kg_dia: IndexError - {product_name} - {result[product_id]}")
            return None
        
        try:
            number = float(price_str)
            result.update({product_id: number * product_quantity})
        except Exception as e:
            result.update({product_id: 0})
            print(f"SCRAPPING_SERVICE - dia.py - get_price_by_kg_dia: match is None - {product_name} - {result[product_id]} - {price_str}")
    else:
        print(f"SCRAPPING_SERVICE - dia.py - get_price_by_kg_dia: status is None - {product_name} - no url")

def get_price_by_unit_dia(product, result, driver, prod_url, status):
    product_name = product["name"]
    product_id = str(product["product_id"])
    product_quantity = product["quantity"]
    if status() == True:
        driver.get(prod_url)
        driver.implicitly_wait(10)
        page = BeautifulSoup(driver.page_source, "html.parser")
        container = page.find_all("div", class_="vtex-flex-layout-0-x-flexRowContent--product-unit")
        
        try:
            price_str = container[0].find_all("span", class_="vtex-product-specifications-1-x-specificationValue")[0].get_text()
        except IndexError:
            result.update({product_id: 0})
            print(f"SCRAPPING_SERVICE - dia.py - get_price_by_unit_dia: IndexError - {product_name} - {result[product_id]}")
            return None

        try:
            number = float(price_str)
            result.update({product_id: number / product_quantity})
        except Exception as e:
            result.update({product_id: 0})
            print(f"SCRAPPING_SERVICE - dia.py - get_price_by_unit_dia: cannot float - {product_name} - {result[product_id]} - {price_str}")
    else:
        print(f"SCRAPPING_SERVICE - dia.py - get_price_by_unit_dia: status is None - {product_name} - no url")

def scrap_dia():
    result = {
        "date": get_date_now()
    }

    date = result.get("date")

    already_exists = get_prices(date, market_id = 4)
    if len(already_exists) > 0:
        return {"error": f"Prices for date {date} already exist in the database"}

    products = get_all_products_markets(4)

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
            print(f"SCRAPPING_SERVICE - dia.py - scrap_dia: TimeoutException")
            driver.quit()
            return None

    for product in products:
        prod_url = product.get("url")
        id = product.get("product_id")
        if prod_url is None or prod_url == "" or prod_url.lower() == "nan":
            result.update({id: 0})
            print(f"ERROR - SCRAPPING_SERVICE - dia.py - scrap_dia: {id} - no url")
            continue
        try:
            if product["measurement"] == "kg" or product["measurement"] == "l":
                get_price_by_kg_dia(product, result, driver, prod_url, status)
            elif product["measurement"] == "unit":
                get_price_by_unit_dia(product, result, driver, prod_url, status)
        except Exception as e:
            print(f"ERROR - SCRAPPING_SERVICE - dia.py - scrap_dia: {e} - {id}")

    return result
