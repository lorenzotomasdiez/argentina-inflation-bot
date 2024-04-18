import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

root_dir = os.path.dirname(os.path.realpath(__file__))
basic_basket_list_dir = os.path.join(root_dir, "base", "basic_basket_list.csv")

canasta = pd.read_csv(
  basic_basket_list_dir,
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

tabla = {
  "id": "SERIAL PRIMARY KEY",
  "fecha": "DATE",
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