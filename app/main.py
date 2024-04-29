from flask import Flask
from config import get_config
from routes.backup.backup import backup_bp
from routes.scrapping.scrapping import scrapping_bp
from routes.seed.seed import seed_bp
from routes.telegram.telegram import telegram_bp
from routes.variation.variation import variation_bp
from routes.compare.compare import comparison_bp
from datetime import timedelta

api_port = get_config()["API_PORT"]

app = Flask(__name__)
app.register_blueprint(backup_bp, url_prefix='/backup')
app.register_blueprint(scrapping_bp, url_prefix='/scrapping')
app.register_blueprint(seed_bp, url_prefix='/seed')
app.register_blueprint(telegram_bp, url_prefix='/telegram')
app.register_blueprint(variation_bp, url_prefix='/variation')
app.register_blueprint(comparison_bp, url_prefix='/compare')

app.config['TIMEZONE_OFFSET'] = timedelta(hours=-3)

@app.route('/')
def index():
    return 'Hello World'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=api_port,  debug=True)
