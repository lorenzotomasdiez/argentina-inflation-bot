import pandas as pd
import datetime as dt
from variacion_perso import (
    variacion_personalizada,
    lista_variacion,
    precios,
    lista_larga,
)

from fechas import (
    es_fin_de_mes,
    nombre_mes,
)

def generate_message(lista_cantidad, dia1, dia2):
    """
    La función `mensaje_twitter` genera un mensaje de Twitter con información sobre las variaciones de
    precio en un período de tiempo determinado para una lista de productos.

    :param lista_cantidad: Define cuantos productos se van a imprimir en el mensaje de Twitter.
    :param dia1: El parámetro "dia1" representa el primer día para el cual se desea calcular la
    variación de precios. Debe ser una fecha específica en el formato "AAAA-MM-DD"
    :param dia2: El parámetro "dia2" representa el segundo día para el cual se desea calcular la
    variación de precios. Se utiliza en la función "mensaje_twitter" para calcular la variación entre
    "dia1" y "dia2" y generar los mensajes correspondientes
    :return: The function `mensaje_twitter` returns four values: `mensaje`, `mensaje_max`,
    `mensaje_min`, and `no_disponible`.
    """
    variacion = variacion_personalizada(dia1, dia2)
    lista = lista_variacion(dia1, dia2, lista_cantidad)

    # obtengo los productos con mas y menor variacion
    no_disponible = ""

    try:
        max = lista[0]
        min = lista[1]

        # productos con precio cero o no disponibles
        productos = precios(lista_larga, dia1, dia2)[1]
        if isinstance(productos, pd.DataFrame):
            productos_no_disponibles = productos.loc[
                productos["precio"] == 0, "producto"
            ].tolist()
            no_disponible = ", ".join(productos_no_disponibles)
            print(f"Los productos sin precio son: {no_disponible}")
        else:
            productos_no_disponibles = []
            no_disponible = f"No hay productos sin precios el dia {dt.datetime.now().day} de {nombre_mes}."
            print(no_disponible)

        # saco los guines bajos de los nombres de los productos
        max = {k.replace("_", " "): v for k, v in max.items()}
        min = {k.replace("_", " "): v for k, v in min.items()}

        # saco los productos con variacion cero
        max = {k: v for k, v in max.items() if v != 0.00}
        min = {k: v for k, v in min.items() if v != 0.00}

        if max == {}:  # si no hay variacion
            max = None
        if min == {}:  # si no hay variacion
            min = None

        print(max)
        print(min)
    except:
        max = None
        min = None

    # si no hay precios del dia actual
    if precios(lista_larga, dia1, dia2)[0] is False:
        mensaje = f"No hay precios del dia {dt.datetime.now().day} de {nombre_mes}."
        mensaje_max = None
        mensaje_min = None

        return mensaje, mensaje_max, mensaje_min, no_disponible

    # si es fin de mes y hay precios del dia actual
    elif es_fin_de_mes:
        mensaje = f"La variación de precios de la canasta básica en el mes de {nombre_mes} es del {variacion[0]}%."
        mensaje_max = f"Los productos con mayor variación del mes de {nombre_mes} son: "
        if max is not None:
            mensaje_max += ", ".join(
                [
                    f"\n{variacion:.2f}% para {producto}"
                    for producto, variacion in max.items()
                ]
            )

        else:
            mensaje_max = (
                mensaje_max + " No hay productos con aumento de precios aun. :)"
            )

        mensaje_min = (
            f"Los productos que más redujeron su precio en el mes de {nombre_mes} son: "
        )
        if min is not None:
            mensaje_min += ", ".join(
                [
                    f"\n{variacion:.2f}% para {producto}"
                    for producto, variacion in min.items()
                ]
            )

        else:
            mensaje_min = (
                mensaje_min + " No hay productos con reduccion de precios aun. :("
            )

        return mensaje, mensaje_max, mensaje_min, no_disponible

    # si no es fin de mes y hay precios del dia actual
    else:
        mensaje = f"La variación de precios de la canasta básica en el mes de {nombre_mes} al día {dt.datetime.now().day} es del {variacion[0]}%."
        mensaje_max = f"Los productos con mayor aumento de {nombre_mes} al día de hoy {dt.datetime.now().day} son:"
        if max is not None:
            mensaje_max += ", ".join(
                [
                    f"\n{variacion:.2f}% para {producto}"
                    for producto, variacion in max.items()
                ]
            )

        else:
            mensaje_max = (
                mensaje_max + " No hay productos con aumento de precios aun. :)"
            )
        mensaje_min = f"Los productos con mayor reducción de precio en el mes de {nombre_mes} al día de hoy {dt.datetime.now().day} son:"
        if min is not None:
            mensaje_min += ", ".join(
                [
                    f"\n{variacion:.2f}% para {producto}"
                    for producto, variacion in min.items()
                ]
            )

        else:
            mensaje_min = (
                mensaje_min + " No hay productos con reduccion de precios aun. :("
            )

        return mensaje, mensaje_max, mensaje_min, no_disponible