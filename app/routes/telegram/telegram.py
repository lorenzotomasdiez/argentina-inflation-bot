from services.telegram.variation import send_general_variation
from services.telegram.send import send_message
from flask import Blueprint, request

telegram_bp = Blueprint('telegram', __name__)

@telegram_bp.route('/test', methods=['GET'])
def test():
    return 'Test Telegram'

@telegram_bp.route('/send', methods=['POST'])
def send():
    message = request.json.get('message')
    return send_message(message)

@telegram_bp.route('/variation/<int:market_id>', methods=['POST'])
def variation(market_id):
    return send_general_variation(market_id)