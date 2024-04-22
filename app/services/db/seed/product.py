import psycopg2
import json
import pandas as pd
from config import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER, basic_basket_list_dir

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
            format_name VARCHAR(255),
            product_type VARCHAR(50),
            portion VARCHAR(50)
        )
        """
    )

    df = pd.read_csv(basic_basket_list_dir, sep=";", encoding="utf-8")

    for row in df.itertuples():
        portion_value = row.porcion
        if pd.isna(row.porcion):
            portion_value = None  # Usar None para NULL en la base de datos

        cursor.execute(
            """
            INSERT INTO products (name, format_name, product_type, portion)
            VALUES (%s, %s, %s, %s)
            """,
            (row.producto, row.producto.strip().replace(' ', '_').lower(),row.tipo_producto, portion_value)
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
            "product_type": product[3],
            "portion": product[4]
        }
        products_json.append(product_dict)

    # Close cursor and connection
    cursor.close()
    connection.close()

    return products_json
