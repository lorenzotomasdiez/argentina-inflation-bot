import re
import datetime as dt
from config import SELENIUM_HOST, SELENIUM_PORT
from services.db.products_markets.index import get_all_products_markets
from services.db.prices.index import get_prices
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from selenium.common.exceptions import TimeoutException # type: ignore
from config import SELENIUM_HOST, SELENIUM_PORT
from bs4 import BeautifulSoup

def get_price_by_kg_dia(driver, prod_url, status):
    if status() == True:
        driver.get(prod_url)
        driver.implicitly_wait(10)
        page = BeautifulSoup(driver.page_source, "html.parser")
        container = page.find_all("div", class_="vtex-flex-layout-0-x-flexRowContent--product-unit")
        price_str = container[0].find_all("span", class_="vtex-product-specifications-1-x-specificationValue")[0].get_text()
        return price_str

def get_price_by_unit_dia(driver, prod_url, status):
    if status() == True:
        driver.get(prod_url)
        driver.implicitly_wait(10)
        page = BeautifulSoup(driver.page_source, "html.parser")
        container = page.find_all("div", class_="vtex-flex-layout-0-x-flexRowContent--product-unit")
        price_str = container[0].find_all("span", class_="vtex-product-specifications-1-x-specificationValue")[0].get_text()
        return price_str


def get_price_by_l_dia(driver, prod_url, status):
    if status() == True:
        driver.get(prod_url)
        driver.implicitly_wait(10)
        page = BeautifulSoup(driver.page_source, "html.parser")
        container = page.find_all("div", class_="vtex-flex-layout-0-x-flexRowContent--product-unit")
        price_str = container[0].find_all("span", class_="vtex-product-specifications-1-x-specificationValue")[0].get_text()
        return price_str


def scrap_dia():
    result = {
        "date": dt.datetime.now().strftime("%Y-%m-%d")
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
            if product["measurement"] == "kg":
                price = get_price_by_kg_dia(driver, prod_url, status)
                if price is not None:
                    result[str(id)] = price
            elif product["measurement"] == "unit":
                price = get_price_by_unit_dia(driver, prod_url, status)
                if price is not None:
                    result[str(id)] = price
            elif product["measurement"] == "l":
                price = get_price_by_l_dia(driver, prod_url, status)
                if price is not None:
                    result[str(id)] = price
        except Exception as e:
            print(f"ERROR - SCRAPPING_SERVICE - dia.py - scrap_dia: {e} - {id}")


    return result
