from services.variation.variation import calculate_products_more_variation, calculate_variation
from flask import Blueprint
import datetime as dt

variation_bp = Blueprint('variation', __name__)

@variation_bp.route('/calculate/<int:market_id>', methods=['GET'])
def calculate(market_id):
    return calculate_variation(market_id)


@variation_bp.route('/calculate/more/<int:market_id>', methods=['GET'])
def calculate_more(market_id):
    return calculate_products_more_variation(market_id)

@variation_bp.route('/calculate/more/<int:market_id>/<string:date_today>', methods=['GET'])
def calculate_more_with_date(market_id, date_today=None):
    if date_today is None:
        date_today = dt.datetime.now().strftime('%Y-%m-%d')
    return calculate_products_more_variation(market_id, date_today)