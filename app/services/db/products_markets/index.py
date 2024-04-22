from config import get_db_connection

def get_all_products_markets(market_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT pm.id, pm.market_id, pm.product_id, pm.quantity, pm.url,
               p.name, p.format_name, p.product_type, p.portion
        FROM products_markets pm
        INNER JOIN products p ON pm.product_id = p.id
        WHERE pm.market_id = %s
        """,
        (market_id,)
    )

    products_markets = cursor.fetchall()

    products_markets_json = []

    for product_market in products_markets:
        product_market_json = {
            "id": product_market[0],
            "market_id": product_market[1],
            "product_id": product_market[2],
            "quantity": product_market[3],
            "url": product_market[4],
            "name": product_market[5],
            "format_name": product_market[6],
            "product_type": product_market[7],
            "portion": product_market[8]
        }
        products_markets_json.append(product_market_json)

    return products_markets_json
