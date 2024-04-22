from flask import Blueprint
from services.db.seed.index import seed_data

seed_bp = Blueprint('seed', __name__)

@seed_bp.route('/', methods = ['POST'])
def index():
    return seed_data()
