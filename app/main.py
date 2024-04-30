from flask import Flask
from config import API_PORT
from routes.backup.backup import backup_bp
from routes.scrapping.scrapping import scrapping_bp
from routes.seed.seed import seed_bp
from routes.telegram.telegram import telegram_bp
from routes.variation.variation import variation_bp
from routes.compare.compare import comparison_bp
from datetime import timedelta
import os

app = Flask(__name__)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app.secret_key = 'nivos'
app.register_blueprint(backup_bp, url_prefix='/backup')
app.register_blueprint(scrapping_bp, url_prefix='/scrapping')
app.register_blueprint(seed_bp, url_prefix='/seed')
app.register_blueprint(telegram_bp, url_prefix='/telegram')
app.register_blueprint(variation_bp, url_prefix='/variation')
app.register_blueprint(comparison_bp, url_prefix='/compare')

app.config['TIMEZONE_OFFSET'] = timedelta(hours=-3)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=API_PORT,  debug=True)
