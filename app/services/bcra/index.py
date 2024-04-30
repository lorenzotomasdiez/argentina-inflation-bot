import datetime as dt
from .variables import get_variables, get_variable_by_id
from .messages import generate_messages
from config import get_date_now
from services.twitter.index import tweet_bcra

def index():
  #http to bcra api
  try:
    variables = get_variables()
    messages = generate_messages(variables)
    return messages
  
  except Exception as e:
    return {
      "error": str(e)
    }

def variable_by_id(id, from_var, to_var):
  try:
    result = get_variable_by_id(id, from_var, to_var)
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
      variable = get_variable_by_id(id, first_day_month, today)
      #variable is an array of results, we need to take the last one
      variables.append(variable[-1])
    
    messages = generate_messages(variables)
    return messages
  
  except Exception as e:
    return {
      "error": str(e)
    }
    
def tweet_today():
  try:  
    messages = general_variables_today()
    for message in messages:
      if(message is not None):
        prefix = "‼️ ACTUALIZACION BCRA ‼️"
        final_message = f"{prefix}\n{message[1]}"
        tweet_bcra(final_message)
      else:
        print(f"Message is None")
    return True
  except Exception as e:
    return {
      "error": str(e)
    }