from flask import Flask, session, request, redirect
from config import get_config
from routes.backup.backup import backup_bp
from routes.scrapping.scrapping import scrapping_bp
from routes.seed.seed import seed_bp
from routes.telegram.telegram import telegram_bp
from routes.variation.variation import variation_bp
from routes.compare.compare import comparison_bp
from routes.bcra.bcra import bcra_bp
from datetime import timedelta
from celeryconfig import celery
import tweepy
import os
from config import X_BCRA_CLIENT_ID, X_BCRA_CLIENT_SECRET


auth = tweepy.OAuth2UserHandler(
    client_id=X_BCRA_CLIENT_ID,
    redirect_uri='http://localhost:3000/oauth/callback',
    scope=["tweet.read", "tweet.write"],
    client_secret=X_BCRA_CLIENT_SECRET
)

api_port = get_config()["API_PORT"]

app = Flask(__name__)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app.secret_key = 'nivos'
app.register_blueprint(backup_bp, url_prefix='/backup')
app.register_blueprint(scrapping_bp, url_prefix='/scrapping')
app.register_blueprint(seed_bp, url_prefix='/seed')
app.register_blueprint(telegram_bp, url_prefix='/telegram')
app.register_blueprint(variation_bp, url_prefix='/variation')
app.register_blueprint(comparison_bp, url_prefix='/compare')
app.register_blueprint(bcra_bp, url_prefix='/bcra')

app.config['TIMEZONE_OFFSET'] = timedelta(hours=-3)
celery.conf.update(app.config)

@app.route('/oauth/callback', methods=['GET', 'POST'])
def twitter_callback():
    access_token = auth.fetch_token(request.url)
    session['twitter_access_token'] = access_token['access_token']
    print(access_token)

    return redirect('/')

@app.route('/twitter-login', methods=['GET', 'POST'])
def twitter_login():
    twitter_login_url = auth.get_authorization_url()
    return redirect(twitter_login_url,code=302)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=api_port,  debug=True)
