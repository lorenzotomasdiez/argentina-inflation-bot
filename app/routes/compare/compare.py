from flask import Blueprint
from services.comparison.compare import compare_markets

comparison_bp = Blueprint('comparison', __name__)

@comparison_bp.route('/general', methods = ['GET'])
def general():
  compare_markets()
  return {"success": "Comparison Done"}