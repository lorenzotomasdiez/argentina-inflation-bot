from flask import Blueprint
from services.scrapping.index import scrapping_test, scrap

scrapping_bp = Blueprint('scrapping', __name__)

@scrapping_bp.route('/test', methods=['GET'])
def test():
    return scrapping_test()

@scrapping_bp.route('/', methods=['POST'])
def index():
    return scrap()
