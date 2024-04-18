import os
import shutil
import datetime

"""
 This function will be used to backup the csv and excel files
"""

def backup_local_csv_xslx():
  date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
  try:
    # Create the backup directory if it doesn't exist
    if not os.path.exists('/app/base/backup'):
      os.makedirs('/app/base/backup')

    # Copiar los archivos al directorio de backup
    shutil.copy(
      os.path.join('/app/base', "prices.csv"),
      os.path.join('/app/base/backup', f"prices{date}.csv"),
    )
    shutil.copy(
      os.path.join('/app/base', "prices.xlsx"),
      os.path.join('/app/base/backup', f"prices{date}.xlsx"),
    )
    shutil.copy(
      os.path.join('/app/base', "prices_long_list.csv"),
      os.path.join('/app/base/backup', f"prices_long_list{date}.csv"),
    )
  except Exception as e:
    print(f"Error during backup_prices() function: {e}")
    return

  return "backup_local_csv_xslx function successfully done"
