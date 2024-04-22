from services.variation.variation import calculate_products_more_variation, calculate_variation
from flask import Blueprint, request
import datetime as dt

variation_bp = Blueprint('variation', __name__)

@variation_bp.route('/calculate', methods=['GET'])
def calculate():
    return calculate_variation()


@variation_bp.route('/calculate/more', methods=['GET'])
def calculate_more():
    return calculate_products_more_variation()

@variation_bp.route('/calculate/more/<string:date_today>', methods=['GET'])
def calculate_more_with_date(date_today=None):
    if date_today is None:
        date_today = dt.datetime.now().strftime('%Y-%m-%d')
    return calculate_products_more_variation(date_today)
