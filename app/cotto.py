import re
from bs4 import BeautifulSoup
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from selenium.common.exceptions import TimeoutException # type: ignore
from config import SELENIUM_HOST, tabla

import datetime as dt


listado = {
  "fecha": dt.datetime.now().strftime("%Y-%m-%d")
}  # diccionario con los precios de los productos

index_error = []

def kilo(nombre_producto, pagina, porcion=1):
    """
    Toma un nombre de producto y una URL, y devuelve el precio del producto.

    :param nombre_producto: El nombre del producto
    :param producto_url: La URL del producto
    :param porcion: la cantidad del producto que desea comprar, defaults to 1 (optional)
    :return: el valor de la variable "listado"
    """
    # pagina = BeautifulSoup(producto_url.page_source, "html.parser")
    # pagina = pagina.get_text
    product_info_container = pagina.find_all("div", id="productInfoContainer")
    disponibilidad = product_info_container[0].find_all(
        "div", class_="product_not_available"
    )

    disponibilidad = product_info_container[0].find_all(
        "div", class_="product_not_available"
    )

    nombre = nombre_producto.replace(" ", "_")
    if nombre == "SalchichÂ¢n":
        nombre = "salchich¢n"

    if disponibilidad:
        listado.update({nombre: 0})
        print(f"{nombre} no disponible, {listado[nombre]}")
        return None

    try:
        # busco dentro de product_info_container el span con la clase unit
        valor = product_info_container[0].find_all("span", class_="unit")[0].get_text()
    except IndexError:
        listado.update({nombre: 0})
        index_error.append(nombre)
        print(f"{nombre} IndexError, {listado[nombre]}")
        return None

    match = re.search(r"\$([\d,.]+)", valor)

    if match:
        number = float(match.group(1).replace(".", "").replace(",", "."))
        print(nombre, (number * porcion))

        listado.update({nombre: number * porcion})
    else:
        listado.update({nombre: 0})
        print("No se encontró un número en el string")

def unidad(nombre_producto, pagina):
    """
    Toma un nombre de producto y una URL, y devuelve el precio del producto.

    :param nombre_producto: nombre del producto
    :param producto_url: La URL del producto
    :return: el valor de la variable "número"
    """
    # pagina = BeautifulSoup(producto_url.page_source, "html.parser")
    # pagina = pagina.get_text
    product_info_container = pagina.find_all("div", id="productInfoContainer")
    # dentro del product_info_container busco el div con la clase product_not_available
    disponibilidad = product_info_container[0].find_all(
        "div", class_="product_not_available"
    )

    nombre = nombre_producto.replace(" ", "_")
    if nombre == "SalchichÂ¢n":
        nombre = "salchich¢n"
    print(f"El nombres es {nombre}")

    if disponibilidad:
        listado.update({nombre: 0})
        print(f"{nombre} no disponible, {listado[nombre]}")
        return None

    try:
        valor = (
            product_info_container[0]
            .find_all("span", class_="atg_store_newPrice")[0]
            .get_text()
        )
    except IndexError:
        listado.update({nombre: 0})
        index_error.append(nombre)
        print(f"{nombre} IndexError, {listado[nombre]}")
        return None

    match = re.search(r"\$([\d,.]+)", valor)

    if match:
        number = float(match.group(1).replace(".", "").replace(",", "."))
        print(nombre, number)
        listado.update({nombre: number})

    else:
        listado.update({nombre: 0})
        print("No se encontró un número en el string")


def scrap_cotto(canasta):
    """
    Toma un marco de datos como entrada, y para cada fila en el marco de datos, llama a una función que
    extrae un sitio web y devuelve un valor.

    :param canasta: un marco de datos con los productos a raspar
    """
    # chromedriver path
    remote_webdriver = SELENIUM_HOST

    # Instantiate ChromeOptions
    chrome_options = webdriver.ChromeOptions()

    # Activate headless mode
    chrome_options.add_argument("--headless=new")

    # Instantiate a webdriver instance
    # driver = webdriver.Chrome(options=chrome_options, executable_path=chromedriver)
    driver = webdriver.Remote(f"{remote_webdriver}:4444/wd/hub", options=chrome_options)

    def status():
        try:
            status = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            return True
        except TimeoutException:
            print("TimeoutException")
            driver.quit()
            return None

    for producto in canasta.index:
        if canasta.loc[producto, "tipo_producto"] == "kilo":

            if status() == True:
                print(canasta.loc[producto, "url_coto"])
                driver.get(canasta.loc[producto, "url_coto"])

                driver.implicitly_wait(10)
                pagina = BeautifulSoup(driver.page_source, "html.parser")

                kilo(canasta.loc[producto, "producto"], pagina)
            else:
                print("no hay url")

        elif canasta.loc[producto, "tipo_producto"] == "unidad":
            # dejo la verificacion en false para que no me de error de certificado pero no es la mejor practica

            if status() == True:
                print(canasta.loc[producto, "url_coto"])
                driver.get(canasta.loc[producto, "url_coto"])

                driver.implicitly_wait(10)
                pagina = BeautifulSoup(driver.page_source, "html.parser")

                unidad(canasta.loc[producto, "producto"], pagina)
            else:
                print("no hay url")

        else:
            canasta.loc[producto, "url_coto"] = "nan"
            print(producto, "no hay url")
    if "nan" in listado.values():
        print("hay un Nan en el diccionario")
    print(f"Listado desde scrappin \n{listado}")

    for producto in listado:
        if producto == "fecha":
            continue
        tabla[producto] = "FLOAT"
