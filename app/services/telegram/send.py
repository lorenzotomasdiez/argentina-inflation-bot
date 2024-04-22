import requests
from config import TELEGRAM_API, TELEGRAM_CHAT_ID

def send_message(message):
    send_text = (
        "https://api.telegram.org/bot"
        + TELEGRAM_API
        + "/sendMessage?chat_id="
        + TELEGRAM_CHAT_ID
        + "&parse_mode=Markdown&text="
        + message
    )
    response = requests.get(send_text)
    return response.json()
