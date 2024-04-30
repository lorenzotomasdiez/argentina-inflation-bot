from flask import Blueprint
from services.scrapping.index import scrap, single_scrap_cotto

scrapping_bp = Blueprint('scrapping', __name__)

@scrapping_bp.route('/', methods=['POST'])
def index():
    return scrap()

# Endpoint for scrapping prices of cotto
@scrapping_bp.route('/cotto', methods=['GET'])
def cotto():
    return single_scrap_cotto()

