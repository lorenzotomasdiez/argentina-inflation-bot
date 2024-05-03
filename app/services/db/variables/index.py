import datetime as dt
from config import get_db_connection
from services.bcra.variables import api_variables

def get_variables_enabled():
  connection = get_db_connection()
  cursor = connection.cursor()
  
  cursor.execute(
    """
    SELECT * FROM bcra_variables WHERE enabled = TRUE
    """
  )
  
  variables = cursor.fetchall()

  variables_json = []
  
  for variable in variables:
    variable_dict = {
      "id": variable[0],
      "description": variable[1],
      "enabled": variable[2],
      "value": variable[3],
      "date": variable[4],
      "last_publish": variable[5]
    }
    variables_json.append(variable_dict)
    
  cursor.close()
  
  return variables_json

def get_variables_enabled_non_published():
  connection = get_db_connection()
  cursor = connection.cursor()
  
  ## SELECT ALL WHERE ENABLED TRUE AND DATE != LAST_PUBLISH
  
  cursor.execute(
    """
    SELECT * FROM bcra_variables WHERE enabled = TRUE AND date != last_publish
    """
  )
  
  variables = cursor.fetchall()

  variables_json = []
  
  for variable in variables:
    variable_dict = {
      "id": variable[0],
      "description": variable[1],
      "enabled": variable[2],
      "value": variable[3],
      "date": variable[4],
      "last_publish": variable[5]
    }
    variables_json.append(variable_dict)
    
  cursor.close()
  
  return variables_json

def update_variables_date():
  variables = api_variables()
  try:
    connection = get_db_connection()
    cursor = connection.cursor()
    
    for variable in variables:
      cursor.execute(
        """
        UPDATE bcra_variables SET value = %s, date = %s WHERE id = %s
        """,
        (variable["valor"], variable["fecha"], variable["idVariable"])
      )
      
    connection.commit() 
    cursor.close()
    connection.close()
    
    return True
  except Exception as e:
    print(e)
    return False
  

def update_variables_last_publish(variables):
  try:
    connection = get_db_connection()
    cursor = connection.cursor()
    
    for variable in variables:
      cursor.execute(
        """
        UPDATE bcra_variables SET last_publish = %s WHERE id = %s
        """,
        (variable["date"], variable["id"])
      )
      
    connection.commit()
    cursor.close()
    connection.close()
    
    return True
  except Exception as e:
    print(e)
    return False
  