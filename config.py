import pandas as pd

import os

script_dir = os.path.dirname(os.path.realpath(__file__))
basic_basket_list_dir = os.path.join(script_dir, "base", "basic_basket_list.csv")

canasta = pd.read_csv(
  basic_basket_list_dir,
  sep=";",
  encoding="utf-8",
  usecols=["producto", "cantidad_g_ml", "url_coto", "tipo_producto", "porcion"],
)

remote_chromedriver = "http://localhost"

psql_host = "localhost"

psql_port = "5432"

tabla = {
  "id": "SERIAL PRIMARY KEY",
  "fecha": "DATE",
} 

