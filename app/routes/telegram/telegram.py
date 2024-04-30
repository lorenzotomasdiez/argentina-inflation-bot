import datetime as dt
from services.telegram.bcra import send_bcra_message
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

@telegram_bp.route('/variation/<int:market_id>/<string:date_today>', methods=['POST'])
def variation_with_date(market_id, date_today=None):
    if date_today is None:
        date_today = dt.datetime.now().strftime('%Y-%m-%d')
    return send_general_variation(market_id, date_today)

@telegram_bp.route("/bcra/today")
def bcra_today():
    send_bcra_message()
    return "Messages sent", 200
