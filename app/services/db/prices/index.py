from config import get_db_connection

class DBPricesServiceError(Exception):
    """Generic exception for errors in the database prices service."""
    pass

def add_prices(prices, market_id):
    date = prices.get("date")
    if not date:
        return {"error": "Missing date in prices data"}, 400

    already_exists = get_prices(date)
    if already_exists:
        return {"error": f"Prices for date {date} already exist in the database"}, 409

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        for key, value in prices.items():
            if key != "date":  # Exclude the "date" key from the loop
                cursor.execute(
                    """
                    INSERT INTO prices (product_id, market_id, price, date)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (int(key), market_id, value, date),
                )

        connection.commit()

        results = get_prices(date)
        return results

    except Exception as e:
        error_message = f"Error in DB-PRICES SERVICE: {e}"
        print(error_message)
        return {"error": error_message}  # Status Code 500: Internal Server Error

    finally:
        cursor.close()
        connection.close()


def get_prices(date):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM prices WHERE date = %s
            """,
            (date,)
        )

        results = cursor.fetchall()

        results_json = []
        for result in results:
            results_json.append({
                "id": result[0],
                "product_id": result[1],
                "market_id": result[2],
                "price": result[3],
                "date": result[4]
            })

        return results_json

    except Exception as e:
        error_message = f"Error in DB-PRICES SERVICE: {e}"
        print(error_message)
        return {"error": error_message}  # Status Code 500: Internal Server Error

    finally:
        cursor.close()
        connection.close()


def get_prices_by_product_dates(product_id, market_id, from_date, to_date):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM prices
            WHERE product_id = %s AND market_id = %s AND date BETWEEN %s AND %s
            """,
            (product_id, market_id, from_date, to_date)
        )

        results = cursor.fetchall()

        results_json = []
        for result in results:
            results_json.append({
                "id": result[0],
                "product_id": result[1],
                "market_id": result[2],
                "price": result[3],
                "date": result[4]
            })

        return results_json
    except Exception as e:
        error_message = f"Error in DB-PRICES SERVICE: {e}"
        print(error_message)
        return {"error": error_message}
    finally:
        cursor.close()
        connection.close()
