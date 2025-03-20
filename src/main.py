from flask import Flask, redirect, url_for, session, jsonify
from authlib.integrations.flask_client import OAuth
import os
import json

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")

# Load credentials from client secret JSON file
with open("client_secret.json") as f:
    credentials = json.load(f)["web"]

# OAuth configuration
oauth = OAuth(app)
app.config['GOOGLE_CLIENT_ID'] = credentials.get("client_id")
app.config['GOOGLE_CLIENT_SECRET'] = credentials.get("client_secret")

discovery_url = "https://accounts.google.com/.well-known/openid-configuration"

# Register the Google OAuth client
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    server_metadata_url=discovery_url,
    client_kwargs={
        'scope': 'openid email profile',
        'prompt': 'consent'
    }
)

@app.route('/')
def home():
    user = session.get('user')
    if user:
        return jsonify(user)
    return '<a href="/login">Login with Google</a>'

@app.route('/login')
def login():
    return google.authorize_redirect(url_for('authorize', _external=True))

@app.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    user_info = google.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
    session['user'] = user_info
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
