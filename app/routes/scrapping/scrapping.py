from flask import Blueprint
from services.scrapping.index import scrapping_test, scrap, single_scrap_carrefour

scrapping_bp = Blueprint('scrapping', __name__)

@scrapping_bp.route('/test', methods=['GET'])
def test():
    return scrapping_test()

@scrapping_bp.route('/', methods=['POST'])
def index():
    return scrap()


@scrapping_bp.route('/carrefour', methods=['POST'])
def carrefour():
    return single_scrap_carrefour()
