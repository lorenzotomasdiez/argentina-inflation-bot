import services.bcra.index as bcra
from .send import send_message
def send_bcra_message():
  try:  
    messages = bcra.general_variables_today()
    for message in messages:
      if(message is not None):
        prefix = "‼️ ACTUALIZACION BCRA ‼️"
        final_message = f"{prefix}\n{message[1]}"
        send_message(final_message)
      else:
        print(f"Message is None")
    return True
  except Exception as e:
    return {
      "error": str(e)
    }