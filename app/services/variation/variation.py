import datetime as dt
from services.db.products.index import get_all_products
import pandas as pd # type: ignore
from services.db.prices.index import get_prices_by_product_dates
from services.db.products_markets.index import get_all_products_markets
from config import get_date_now

def calculate_variation(market_id, today=None):
    if today is None:
        today = get_date_now()

    first_day_month = dt.datetime.strptime(today, '%Y-%m-%d').replace(day=1).strftime('%Y-%m-%d')

    products = get_all_products_markets(market_id)

    product_variations = []

    for product in products:
        product_id = product["product_id"]
        market_id = product["market_id"]
        prices = get_prices_by_product_dates(product_id, market_id, first_day_month, today)
        if "error" in prices or isinstance(prices, dict):
            raise Exception("Error in DB-PRICES SERVICE")
            continue
        if len(prices) > 1:
            first_price = prices[0].get("price")
            last_price = prices[-1].get("price")
            if first_price == 0 or last_price == 0:
                continue
            product_variation = {
                "product_id": product_id,
                "market_id": market_id,
                "first": first_price,
                "last": last_price,
            }
            product_variations.append(product_variation)


    df = pd.DataFrame(product_variations)

    if df.empty:
        raise Exception("Empty DataFrame")

    df_last_prices = df[['last']]['last']

    df_first_prices = df[['first']]['first']

    price_variation = round(((df_last_prices - df_first_prices) / df_first_prices) * 100, 2)

    average_variation = price_variation.mean()

    return {
        "products": product_variations,
        "price_variation": average_variation,
        "from": first_day_month,
        "to": today
    }


def calculate_products_more_variation(market_id, today=None):
    complete_products = get_all_products()
    variation = calculate_variation(market_id, today)

    products = variation.get("products")
    from_var = variation.get("from")
    to_var = variation.get("to")

    if products is None or len(products) < 1:
        return {
            "products": [],
            "price_variation": None,
            "date": today
        }

    result = products

    for product in result:
        for complete_product in complete_products:
            if product["product_id"] == complete_product["id"]:
                product["name"] = complete_product["name"]
                product["variation"] = round((product["last"] / product["first"] - 1) * 100, 2)
                break

    result_sorted = sorted(result, key=lambda x: x["variation"], reverse=True)

    df_variations = pd.DataFrame(result_sorted)[['variation']]['variation']

    df_variations_mean = df_variations.mean()

    return {
        "products": result_sorted,
        "price_variation": df_variations_mean,
        "from": from_var,
        "to": to_var
    }
