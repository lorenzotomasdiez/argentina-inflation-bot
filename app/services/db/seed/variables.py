from config import get_db_connection
from services.bcra.variables import api_variables
def create_bcra_variables():
  connection = get_db_connection()
  cursor = connection.cursor()

  cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS bcra_variables (
      id SERIAL PRIMARY KEY,
      description VARCHAR(255) NOT NULL,
      enabled BOOLEAN DEFAULT FALSE,
      value VARCHAR(255) NOT NULL,
      date VARCHAR(255) NOT NULL,
      last_publish VARCHAR(255) NOT NULL
    )
    """
  )
  
  variables = api_variables()
  
  enabled_variables = [1, 4, 5, 6, 15, 16, 34]
  
  for variable in variables:
    enabled = variable["idVariable"] in enabled_variables
    cursor.execute(
      """
      INSERT INTO bcra_variables (id, description, enabled, value, date, last_publish) VALUES (%s, %s, %s, %s, %s, %s)
      """,
      (variable["idVariable"], variable["descripcion"], enabled, variable["valor"],variable["fecha"], variable["fecha"])
    )
  
  connection.commit()
  
  cursor.execute(
    """
    SELECT * FROM bcra_variables
    """
  )
  
  psql_variables = cursor.fetchall()
  
  variables_json = []
  
  for variable in psql_variables:
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
  connection.close()
  
  return variables_json
  