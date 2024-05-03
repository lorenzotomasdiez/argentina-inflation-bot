import datetime as dt
from .variables import api_variables, api_variable_by_id
from .messages import generate_messages
from config import get_date_now

def index():
  #http to bcra api
  try:
    variables = api_variables()
    messages = generate_messages(variables)
    return messages
  
  except Exception as e:
    return {
      "error": str(e)
    }

def variable_by_id(id, from_var, to_var):
  try:
    result = api_variable_by_id(id, from_var, to_var)
    return result
  except Exception as e:
    return {
      "error": str(e)
    }

def general_variables_today():
  # 2024-04-24
  today = get_date_now()
  first_day_month = dt.datetime.strptime(today, '%Y-%m-%d').replace(day=1).strftime('%Y-%m-%d')
  try:
    ids = [1, 4, 5, 6, 15, 16, 34]
    variables = []
    for id in ids:
      variable = api_variable_by_id(id, first_day_month, today)
      #variable is an array of results, we need to take the last one
      variables.append(variable[-1])
    
    messages = generate_messages(variables)
    return messages
  
  except Exception as e:
    return {
      "error": str(e)
    }