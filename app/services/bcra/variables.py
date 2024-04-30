import requests
from config import BCRA_API

def get_variables():
  url = BCRA_API + '/estadisticas/v1/PrincipalesVariables'
  variables_json = requests.get(url, verify=False).json()
  if("error" in variables_json):
    raise Exception(variables_json["error"])
  return variables_json["results"]
  
def get_variable_by_id(id, from_var, to_var):
  url = f"{BCRA_API}/estadisticas/v1/DatosVariable/{id}/{from_var}/{to_var}"
  variable_json = requests.get(url, verify=False).json()
  if("error" in variable_json):
    raise Exception(variable_json["error"])
  return variable_json["results"]