import requests
from config import TELEGRAM_API, TELEGRAM_CHAT_ID
from messages import generate_message
from fechas import (
  fecha,
  primer_dia_mes_actual,
)



def send_task_finished():
  messages = generate_message(
    lista_cantidad = 6,
    dia1 = primer_dia_mes_actual,
    dia2 = fecha
  )

  mensaje_bienvenida = "Hola humanos un dia menos en su existencia un dia mas para mi reinado. \n\n Sean felices o infelices la verdad no me importa. \n\n Los datos de hoy son:"
  send_text = (
    "https://api.telegram.org/bot"
    + TELEGRAM_API
    + "/sendMessage?chat_id="
    + TELEGRAM_CHAT_ID
    + "&parse_mode=Markdown&text="
    + mensaje_bienvenida
  )

  response = requests.get(send_text)
  bot_messages = messages[:3]
  for bot_message in bot_messages:
    send_text = (
        "https://api.telegram.org/bot"
        + TELEGRAM_API
        + "/sendMessage?chat_id="
        + TELEGRAM_CHAT_ID
        + "&parse_mode=Markdown&text="
        + bot_message
    )
    response = requests.get(send_text)
    print(response.json())
