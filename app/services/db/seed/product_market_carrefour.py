import psycopg2
import numpy as np
import json
import pandas as pd
import os
from config import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER, base_dir

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
            url, url of the product in the market
        """
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS products_markets (
                id SERIAL PRIMARY KEY,
                product_id INTEGER REFERENCES products(id),
                market_id INTEGER REFERENCES markets(id),
                url VARCHAR(255) NOT NULL,
                measurement VARCHAR(255) NOT NULL DEFAULT 'kg'
            )
            """
        )

        carrefour_dir =  os.path.join(base_dir, "03-list.csv")
        carrefour_df = pd.read_csv(carrefour_dir, sep=";", encoding="utf-8")

        for row in carrefour_df.itertuples():
            # find in products_seeded object the one with the name equal to df.producto
            product = next((product for product in products_seeded if product["format_name"] == row.product), None)
            if product is None:
                continue
            cursor.execute(
                """
                INSERT INTO products_markets (product_id, market_id, url)
                VALUES (%s, %s, %s)
                """,
                (product["id"], 3, row.url)
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
                "url": product_market[3],
            }
            products_markets_json.append(product_market_json)

        cursor.close()
        connection.close()

        return products_markets_json

    except Exception as e:
        return {
            "error": e
        }
