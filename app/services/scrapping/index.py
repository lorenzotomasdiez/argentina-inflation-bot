import json
from .cotto import scrap_cotto
from .dia import scrap_dia
from services.db.prices.index import add_prices
import time

def scrap():
    has_error = False
    coto_results = scrap_cotto()
    if "error" in coto_results:
        has_error = True
        print(coto_results)
    else:
        add_prices(prices = coto_results, market_id = 1)

    
    #wait for 1 minute
    time.sleep(60)
    
    dia_results = scrap_dia()
    if "error" in dia_results:
        has_error = True
        print(dia_results)
    else:
        add_prices(prices = dia_results, market_id = 4)
         
    return {
        "sucess": True,
        "message": has_error if "error" else "Prices added successfully"
    }


def single_scrap_cotto():
    coto_results = scrap_cotto()
    if "error" in coto_results:
        return {
            "sucess": False,
            "message": coto_results
        }
    else:
        return {
            "sucess": True,
            "message": "Prices added successfully"
        }
