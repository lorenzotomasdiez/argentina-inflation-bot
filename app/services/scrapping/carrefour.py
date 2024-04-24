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


def scrap_carrefour():
    result = {
        "date": dt.datetime.now().strftime("%Y-%m-%d")
    }

    date = result.get("date")

    already_exists = get_prices(date, market_id = 3)
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
            print(f"SCRAPPING_SERVICE - carrefour.py - scrap_carrefour: TimeoutException")
            driver.quit()
            return None

    for product in products:
        prod_url = product.get("url")
        if prod_url is None:
            continue
        try:
            if status() == True:
                driver.get(prod_url)
                driver.implicitly_wait(10)
                soup = BeautifulSoup(driver.page_source, "html.parser")

                # Get the price per kilo
                price_per_kilo_container = soup.findAll("div", class_="vtex-flex-layout-0-x-flexRowContent--product-unit")
                try:
                    text = price_per_kilo_container[0].findAll("span", class_="vtex-product-specifications-1-x-specificationValue")[0].get_text()
                except Exception as e:
                    print(f"ERROR - SCRAPPING_SERVICE - carrefour.py - scrap_carrefour: {e}")
                    continue

                print("Precio por kilo:", text)
                result.update({product.get("product_id"): text})
            else:
                print(f"SCRAPPING_SERVICE - carrefour.py - scrap_carrefour: status() == False")

            if "nan" in result.values():
                print(f"ERROR - SCRAPPING_SERVICE - carrefour.py - scrap_carrefour: nan in list")
        except Exception as e:
            print(f"ERROR - SCRAPPING_SERVICE - carrefour.py - scrap_carrefour: {e}")

    return result
