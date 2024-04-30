import datetime as dt
from datetime import timezone
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

root_dir = os.path.dirname(os.path.realpath(__file__))
base_dir = os.path.join(root_dir, "base")
prices_dir = os.path.join(root_dir, "base", "prices.csv")
prices_long_list_dir = os.path.join(root_dir, "base", "prices_long_list.csv")

basket_csv = pd.read_csv(
  os.path.join(base_dir, "old", "basic_basket_list.csv"),
  sep=";",
  encoding="utf-8",
  usecols=["producto", "cantidad_g_ml", "url_coto", "tipo_producto", "porcion"],
)

API_PORT = os.getenv("API_PORT")
TELEGRAM_API = os.getenv("TELEGRAM_API")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
SELENIUM_HOST = os.getenv("SELENIUM_HOST")
SELENIUM_PORT = os.getenv("SELENIUM_PORT")
REDIS_URL = os.getenv("REDIS_URL")

X_BCRA_API_KEY = os.getenv("X_BCRA_API_KEY")
X_BCRA_API_SECRET = os.getenv("X_BCRA_API_SECRET")
X_BCRA_API_ACCESS_TOKEN = os.getenv("X_BCRA_API_ACCESS_TOKEN")
X_BCRA_API_ACCESS_TOKEN_SECRET = os.getenv("X_BCRA_API_ACCESS_TOKEN_SECRET")
X_BCRA_API_BEARER_TOKEN = os.getenv("X_BCRA_API_BEARER_TOKEN")
X_BCRA_CLIENT_ID = os.getenv("X_BCRA_CLIENT_ID")
X_BCRA_CLIENT_SECRET = os.getenv("X_BCRA_CLIENT_SECRET")

X_AHORRO_API_KEY = os.getenv("X_AHORRO_API_KEY")
X_AHORRO_API_SECRET = os.getenv("X_AHORRO_API_SECRET")
X_AHORRO_API_ACCESS_TOKEN = os.getenv("X_AHORRO_API_ACCESS_TOKEN")
X_AHORRO_API_ACCESS_TOKEN_SECRET = os.getenv("X_AHORRO_API_ACCESS_TOKEN_SECRET")
X_AHORRO_API_BEARER_TOKEN = os.getenv("X_AHORRO_API_BEARER_TOKEN")
X_AHORRO_CLIENT_ID = os.getenv("X_AHORRO_CLIENT_ID")
X_AHORRO_CLIENT_SECRET = os.getenv("X_AHORRO_CLIENT_SECRET")

BCRA_API = 'https://api.bcra.gob.ar'

table = {
  "id": "SERIAL PRIMARY KEY",
  "date": "DATE",
}

def get_config():
    return {
        "API_PORT": API_PORT,
        "TELEGRAM_API": TELEGRAM_API,
        "TELEGRAM_CHAT_ID": TELEGRAM_CHAT_ID,
        "POSTGRES_HOST": POSTGRES_HOST,
        "POSTGRES_PORT": POSTGRES_PORT,
        "POSTGRES_USER": POSTGRES_USER,
        "POSTGRES_PASSWORD": POSTGRES_PASSWORD,
        "POSTGRES_DB": POSTGRES_DB,
        "SELENIUM_HOST": SELENIUM_HOST,
        "SELENIUM_PORT": SELENIUM_PORT,
    }


def get_db_connection():
    return psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )

def get_month_from_date(date):
    months = {
        "01": "Enero",
        "02": "Febrero",
        "03": "Marzo",
        "04": "Abril",
        "05": "Mayo",
        "06": "Junio",
        "07": "Julio",
        "08": "Agosto",
        "09": "Septiembre",
        "10": "Octubre",
        "11": "Noviembre",
        "12": "Diciembre",
    }
    month = date.split("-")[1]
    return months.get(month)


def get_date_now():
    """Get the current date in GMT-3 timezone format."""
    # Get the current time in UTC
    current_utc_time = dt.datetime.now(timezone.utc)

    # Calculate the offset for GMT-3 timezone (3 hours west of UTC)
    gmt_minus_three_offset = dt.timedelta(hours=-3)

    # Apply the offset to get the current time in GMT-3 timezone
    current_gmt_minus_three_time = current_utc_time + gmt_minus_three_offset

    # Format the current date in the desired format ("%Y-%m-%d")
    current_date_in_gmt_minus_three_format = current_gmt_minus_three_time.strftime("%Y-%m-%d")

    return current_date_in_gmt_minus_three_format
