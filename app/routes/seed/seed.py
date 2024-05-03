from flask import Blueprint
from services.db.seed.index import seed_data, single_seed_markets, single_seed_products_markets_carrefour, seed_bcra_variables

seed_bp = Blueprint('seed', __name__)

@seed_bp.route('/', methods = ['POST'])
def index():
    return seed_data()

@seed_bp.route('/markets', methods = ['POST'])
def markets():
    return single_seed_markets()

@seed_bp.route('/carrefour/products', methods = ['POST'])
def carrefour_products():
    return single_seed_products_markets_carrefour()

@seed_bp.route('/bcra/variables', methods = ['POST'])
def bcra_variables():
    return seed_bcra_variables()
