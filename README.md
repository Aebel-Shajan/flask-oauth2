# flask-oauth2
Example website that uses google oauth 2.0 and google drive api.

## Pre reqs
* Python
* Node

## Setup

Setup venv
```bash
python3 -m venv .venv
```
Activate venv (linus/macos)
```bash
source .venv/bin/activate
```
(windows)
```bash
.venv\Scripts\activate
```
Install dependencies
```bash
pip install -r requirements.txt
```

Install node modules (only sass :P)
```bash
npm i
```

## Run command
```
python src/main.py & npm run watch-sass
```

## links
https://developers.google.com/identity/protocols/oauth2
https://developers.google.com/drive/api/guides/api-specific-auth
https://flask.palletsprojects.com/en/stable/quickstart/#a-minimal-application
https://jinja.palletsprojects.com/en/stable/templates/