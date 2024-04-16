from handle_database import cargar_ddbb_local, guardar_csv_excel#, cargar_dddb_cloud

from cotto import scrap_cotto, listado
from config import canasta

def scrapping():
  scrap_cotto(canasta)
  # Cargar datos y backup en la base de datos local

  # @task
  # def cargar_todo():
  cargar_ddbb_local(listado)

  # Guardar datos en csv y excel

  guardar_csv_excel()

  # Cargar datos en la base de datos cloud
  #cargar_dddb_cloud(lista_larga)