import psycopg2
import numpy as np
import json
import pandas as pd
from config import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER, basic_basket_list_dir, basic_basket_list_carrefour_dir

def seed_products_markets_carrefour(products_seeded):
    try:
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

        carrefour_df = pd.read_csv(basic_basket_list_carrefour_dir, sep=";", encoding="utf-8")

        carrefour_df["cantidad_g_ml"] = carrefour_df["cantidad_g_ml"].str.replace(",", ".")

        carrefour_df["cantidad_g_ml"] = carrefour_df["cantidad_g_ml"].str.replace("-", "")

        carrefour_df["cantidad_g_ml"].replace('', np.nan, inplace=True)

        carrefour_df["cantidad_g_ml"] = carrefour_df["cantidad_g_ml"].astype(float)

        for row in carrefour_df.itertuples():
            # find in products_seeded object the one with the name equal to df.producto
            product = next((product for product in products_seeded if product["name"] == row.producto), None)
            if product is None:
                continue
            cursor.execute(
                """
                INSERT INTO products_markets (product_id, market_id, quantity, url)
                VALUES (%s, %s, %s, %s)
                """,
                (product["id"], 3, row.cantidad_g_ml, row.url)
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

    except Exception as e:
        return {
            "error": e
        }
