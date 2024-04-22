import psycopg2
from config import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER

def drop_all():
    connection = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )

    cursor = connection.cursor()

    # drop tables with CASCADE to remove dependencies
    cursor.execute(
        """
        DROP TABLE IF EXISTS products_markets CASCADE
        """
    )
    cursor.execute(
        """
        DROP TABLE IF EXISTS products CASCADE
        """
    )
    cursor.execute(
        """
        DROP TABLE IF EXISTS markets CASCADE
        """
    )

    cursor.execute(
        """
        DROP TABLE IF EXISTS prices CASCADE
        """
    )

    connection.commit()
    cursor.close()
    connection.close()

    return True
