from services.telegram.send import send_message
from flask import Blueprint, request

telegram_bp = Blueprint('telegram', __name__)

@telegram_bp.route('/test', methods=['GET'])
def test():
    return 'Test Telegram'

@telegram_bp.route('/send', methods=['POST'])
def send():
    "get message from request and send it to telegram"
    message = request.json.get('message')
    return send_message(message)
