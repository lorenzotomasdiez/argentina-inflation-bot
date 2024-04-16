import os
import shutil
import datetime

script_dir = os.path.dirname(os.path.realpath(__file__))
base_dir = os.path.join(script_dir, "base")
backup_dir = os.path.join(script_dir, "base", "backup")

def backup_prices():
  """
  Hace un backup de los archivos csv y excel
  """        
  # Hacer backup de los archivos csv y excel
  fecha = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
  try:
    # Crear el directorio de backup si no existe
    if not os.path.exists(backup_dir):
      os.makedirs(backup_dir)

    # Copiar los archivos al directorio de backup
    shutil.copy(
      os.path.join(base_dir, "prices.csv"),
      os.path.join(backup_dir, f"prices{fecha}.csv"),
    )
    shutil.copy(
      os.path.join(base_dir, "prices.xlsx"),
      os.path.join(backup_dir, f"prices{fecha}.xlsx"),
    )
    shutil.copy(
      os.path.join(base_dir, "prices_long_list.csv"),
      os.path.join(backup_dir, f"prices_long_list{fecha}.csv"),
    )
  except Exception as e:
    print(f"Error during backup_prices() function: {e}")
    return
  
  print("backup_prices function successfully done")