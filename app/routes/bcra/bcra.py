from flask import Blueprint
import services.bcra.index as bcra

bcra_bp = Blueprint('bcra', __name__)

@bcra_bp.route('/', methods = ['GET'])
def index():
  return bcra.index()

#variables by date
#/estadisticas/v1/DatosVariable/{id}/{from_var}/{to_var}
@bcra_bp.route('/variable/<id>/<from_var>/<to_var>', methods = ['GET'])
def variable(id, from_var, to_var):
  return bcra.variable_by_id(id, from_var, to_var)

@bcra_bp.route('/today', methods = ['GET'])
def today():
  return bcra.general_variables_today()