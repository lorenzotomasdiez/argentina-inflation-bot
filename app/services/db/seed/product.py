import psycopg2
import os
import json
import pandas as pd
from config import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER, base_dir

def seed_products():
    connection = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )

    cursor = connection.cursor()

    #create table if not exists
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            format_name VARCHAR(255) NOT NULL UNIQUE
        )
        """
    )

    products_dir = os.path.join(base_dir, "list.csv")

    df = pd.read_csv(products_dir, sep=";", encoding="utf-8")

    for row in df.itertuples():
        cursor.execute(
            """
            INSERT INTO products (name, format_name)
            VALUES (%s, %s)
            """,
            (row.name, row.product)
        )

    connection.commit()

    cursor.execute(
        """
        SELECT * FROM products
        """
    )
    products = cursor.fetchall()
    products_json = []
    for product in products:
        product_dict = {
            "id": product[0],
            "name": product[1],
            "format_name": product[2],
        }
        products_json.append(product_dict)

    # Close cursor and connection
    cursor.close()
    connection.close()

    return products_json
