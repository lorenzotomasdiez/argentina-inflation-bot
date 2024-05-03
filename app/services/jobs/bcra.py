import datetime as dt
from services.db.variables.index import get_variables_enabled_non_published, update_variables_date, update_variables_last_publish, get_variables_enabled
from services.bcra.messages import generate_messages
from services.bcra.variables import api_variable_by_id
from services.twitter.index import tweet, bcra_client
from services.visualizations.month import generate_graph_month_message
from services.visualizations.government import generate_graph_government
from config import get_date_now

def general():
  try:
    print(f"Running BCRA.py - general() - { dt.datetime.now()}")
    result = update_variables_date()
    if result == False:
      print("BCRA.py - general() - cannot update variables")
    
    variables = get_variables_enabled_non_published()
    
    messages = generate_messages(variables)
    
    clients = bcra_client()
    
    for message in messages:
      if(message is not None):
        prefix = "‼️ ACTUALIZACION BCRA ‼️"
        final_message = f"{prefix}\n{message[1]}"
        tweet(clients, final_message)
    
    update_variables_last_publish(variables)
    message = f"BCRA.py - general() - Finished - { dt.datetime.now()} - Numbers updated {len(variables)}"
    print(message)
    return message
  except Exception as e:
    print(e)
    print("BCRA.py - general() - Error")
  

def graph_month():
  current_date = dt.datetime.now()
  first_day_last_month = dt.datetime(current_date.year, current_date.month - 1, 1)
  last_day_last_month = dt.datetime(current_date.year, current_date.month, 1) - dt.timedelta(days=1)
  first_day_last_month_str = first_day_last_month.strftime("%Y-%m-%d")
  last_day_last_month_str = last_day_last_month.strftime("%Y-%m-%d")

  try:
    variables = get_variables_enabled()
    clients = bcra_client()
    for variable in variables:
      results = api_variable_by_id(variable["id"], first_day_last_month_str, last_day_last_month_str)
      message = generate_graph_month_message(
        variable["id"],
        results,
        first_day_last_month_str
      )
      if(message is not None):
        tweet(clients, message, "graph_month.png")
    
    message = f"BCRA.py - graph_month() - Finished - { dt.datetime.now()} - numbers published {len(variables)}"
    print(message)
    return message
    
  except Exception as e:
    print(e)
    print("BCRA.py - graph_month() - Error")
    

def graph_government():
  try:
    variables = get_variables_enabled()
    clients = bcra_client()
    for variable in variables:
      results = api_variable_by_id(variable["id"], "2023-12-11", get_date_now())
      message = generate_graph_government(
        variable["id"],
        results
      )
      if(message is not None):
        tweet(clients, message, "graph_government.png")
    
    message = f"BCRA.py - graph_government() - Finished - { dt.datetime.now()} - numbers published {len(variables)}"
    return message
    
  except Exception as e:
    print(e)
    print("BCRA.py - graph_month() - Error")
  
def graph_government_by_id(id):
  try:
    variables = get_variables_enabled()
    
    variable = next((x for x in variables if x["id"] == id), None)
    
    results = api_variable_by_id(variable["id"], "2023-12-11", get_date_now())
    
    message = generate_graph_government(
      variable["id"],
      results
    )
    
    return message
    
  except Exception as e:
    print(e)
    print("BCRA.py - graph_month() - Error")