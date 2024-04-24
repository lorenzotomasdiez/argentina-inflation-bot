import psycopg2
import numpy as np
import json
import pandas as pd
from config import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER, basic_basket_list_dir

def seed_products_markets_cotto(products_seeded, markets_seeded):
    connection = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )

    cursor = connection.cursor()

    #create table if not exists
    """
        id,
        product_id, id of the product
        market_id, id of the market
        quantity, quantity in gr or ml
        url, url of the product in the market
        type, type of the product unit or kilo
        portion, portion of the product can be null
    """
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products_markets (
            id SERIAL PRIMARY KEY,
            product_id INTEGER REFERENCES products(id),
            market_id INTEGER REFERENCES markets(id),
            quantity FLOAT NOT NULL,
            url VARCHAR(255) NOT NULL
        )
        """
    )

    coto_df = pd.read_csv(basic_basket_list_dir, sep=";", encoding="utf-8")

    coto_df["cantidad_g_ml"] = coto_df["cantidad_g_ml"].str.replace(",", ".")

    coto_df["cantidad_g_ml"] = coto_df["cantidad_g_ml"].str.replace("-", "")

    coto_df["cantidad_g_ml"].replace('', np.nan, inplace=True)

    coto_df["cantidad_g_ml"] = coto_df["cantidad_g_ml"].astype(float)


    for row in coto_df.itertuples():
        # find in products_seeded object the one with the name equal to df.producto
        product = next((product for product in products_seeded if product["name"] == row.producto), None)
        market = next((market for market in markets_seeded if market["name"] == "coto"), None)
        if product is None:
            continue
        if market is None:
            continue
        cursor.execute(
            """
            INSERT INTO products_markets (product_id, market_id, quantity, url)
            VALUES (%s, %s, %s, %s)
            """,
            (product["id"], market["id"], row.cantidad_g_ml, row.url_coto)
        )

    connection.commit()

    cursor.execute(
        """
        SELECT * FROM products_markets
        """
    )

    products_markets = cursor.fetchall()

    products_markets_json = []

    for product_market in products_markets:
        product_market_json = {
            "id": product_market[0],
            "product_id": product_market[1],
            "market_id": product_market[2],
            "quantity": product_market[3],
            "url": product_market[4],
        }
        products_markets_json.append(product_market_json)

    cursor.close()
    connection.close()

    return products_markets_json
