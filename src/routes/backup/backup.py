from flask import Blueprint

backup_bp = Blueprint('backup', __name__)

@backup_bp.route('/')
def backup():
    return "This is the backup route."

@backup_bp.route('/restore')
def restore_backup():
    return "This is the restore backup route."
