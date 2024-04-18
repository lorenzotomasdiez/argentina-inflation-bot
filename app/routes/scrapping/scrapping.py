from flask import Blueprint

scrapping_bp = Blueprint('scrapping', __name__)

@scrapping_bp.route('/scrapping')
def scrapping():
    return "This is the scrapping route."

@scrapping_bp.route('/scrapping/profile')
def scrapping_profile():
    return "This is the scrapping profile route."
