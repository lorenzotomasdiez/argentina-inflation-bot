from flask import Blueprint
from services.backup.index import backup_test, backup_local_csv

backup_bp = Blueprint('backup', __name__)

@backup_bp.route('/test', methods = ['POST'])
def test():
    return backup_test()

@backup_bp.route('/local-csv', methods = ['POST'])
def local():
    return backup_local_csv()

@backup_bp.route('/restore')
def restore_backup():
    return "This is the restore backup route."
