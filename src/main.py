#from src.backup import backup_prices
#from scrapping import scrapping
#from telegram import send_task_finished
#from src.scrapping import scrapping
import time
from flask import Flask
from config import get_config, root_dir
from routes.backup.backup import backup_bp

api_port = get_config()["API_PORT"]

app = Flask(__name__)
app.register_blueprint(backup_bp, url_prefix='/backup')

@app.route('/')
def index():
    return 'Hello World'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=api_port)

#backup_prices()
#scrapping()
#send_task_finished()
#twittear
