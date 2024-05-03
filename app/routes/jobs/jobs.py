from flask import Blueprint
import services.jobs.ahorro as jobs_ahorro_service
import services.jobs.bcra as jobs_bcra_service
jobs_bp = Blueprint('jobs', __name__)

#AHORRO JOBS
@jobs_bp.route('/ahorro/general', methods = ['GET'])
def ahorro_general():
  jobs_ahorro_service.general()
  return "Ahorro General Job Done"


#BCRA JOBS
@jobs_bp.route('/bcra/general', methods = ['GET'])
def bcra_general():
  return jobs_bcra_service.general()


@jobs_bp.route('/bcra/month', methods = ['GET'])
def bcra_month():
  return jobs_bcra_service.graph_month()


@jobs_bp.route('/bcra/government', methods = ['GET'])
def bcra_government():
  return jobs_bcra_service.graph_government()

#government by id
@jobs_bp.route('/bcra/government/<int:id>', methods = ['GET'])
def bcra_government_by_id(id):
  return jobs_bcra_service.graph_government_by_id(id)

@jobs_bp.route('/bcra/test', methods = ['GET'])
def bcra_test():
  return "other"