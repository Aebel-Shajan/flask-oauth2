from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
import numpy as np
import os
import json
import datetime

server = Flask(__name__)
server.secret_key = os.getenv("SECRET_KEY", "supersecretkey")

# Load credentials from client secret JSON file
with open("client_secret.json") as f:
    credentials = json.load(f)["web"]

# OAuth configuration
oauth = OAuth(server)
server.config['GOOGLE_CLIENT_ID'] = credentials.get("client_id")
server.config['GOOGLE_CLIENT_SECRET'] = credentials.get("client_secret")

discovery_url = "https://accounts.google.com/.well-known/openid-configuration"

# Register the Google OAuth client
google = oauth.register(
    name='google',
    client_id=server.config['GOOGLE_CLIENT_ID'],
    client_secret=server.config['GOOGLE_CLIENT_SECRET'],
    server_metadata_url=discovery_url,
    client_kwargs={
        'scope': 'openid email profile',
        'prompt': 'consent'
    }
)

@server.route('/login')
def login():
    return google.authorize_redirect(url_for('authorize', _external=True))

@server.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    user_info = google.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
    session['user'] = user_info
    return redirect('/')

@server.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

# Create Dash app
dash_app = dash.Dash(__name__, server=server, routes_pathname_prefix='/', suppress_callback_exceptions=True)

# Sample data for scatter plot
df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species", title="Sepal Width vs. Length")

# Generate GitHub-style heatmap data
now = datetime.datetime.now()
dates = pd.date_range(start=now - datetime.timedelta(days=365), periods=365)
data = pd.DataFrame({
    "date": dates,
    "commits": np.random.randint(0, 10, size=365)
})

heatmap_fig = px.density_heatmap(
    data, x=data["date"].dt.isocalendar().week, y=data["date"].dt.weekday, z="commits",
    color_continuous_scale="Blues",
    title="Contribution Heatmap (Past Year)",
    labels={"x": "Week", "y": "Day of Week"}
)

def serve_layout():
    user = session.get('user')
    if user:
        return html.Div([
            html.H1(f'Welcome, {user["name"]}!'),
            html.Img(src=user["picture"], style={'width': '100px', 'border-radius': '50%'}),
            html.Br(),
            html.A('Logout', href='/logout'),
            dcc.Graph(figure=fig),  # Scatter plot
            dcc.Graph(figure=heatmap_fig)  # Heatmap
        ])
    return html.Div([
        html.H1('Please log in'),
        html.A('Login with Google', href='/login')
    ])

dash_app.layout = lambda: serve_layout()

if __name__ == '__main__':
    server.run(debug=True)
