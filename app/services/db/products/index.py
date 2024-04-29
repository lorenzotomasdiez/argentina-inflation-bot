from config import get_db_connection


def get_all_products():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM products
        """
    )

    products = cursor.fetchall()

    products_json = []

    for product in products:
        product_json = {
            "id": product[0],
            "name": product[1],
            "format_name": product[2],
        }
        products_json.append(product_json)


    return products_json
