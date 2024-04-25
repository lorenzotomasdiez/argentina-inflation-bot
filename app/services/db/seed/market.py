import psycopg2
import json
import pandas as pd
import os
from config import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER, base_dir

def seed_markets():
    connection = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )

    cursor = connection.cursor()

    #create table if not exists name should be unique
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS markets (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE
        )
        """
    )

    markets_dir = os.path.join(base_dir, "markets.csv")

    df_markets = pd.read_csv(markets_dir)

    # get markets from csv
    markets_to_seed = df_markets["market"].tolist()

    for market in markets_to_seed:
        cursor.execute(
            """
            INSERT INTO markets (name)
            VALUES (%s)
            """,
            (market,)
        )

    connection.commit()

    cursor.execute(
        """
        SELECT * FROM markets
        """
    )

    markets = cursor.fetchall()
    markets_json = []
    for market in markets:
        markets_json.append({
            "id": market[0],
            "name": market[1]
        })

    return markets_json
