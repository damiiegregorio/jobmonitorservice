from flask import render_template

import config

app = config.connex_app

app.add_api('swagger.yml')


@app.route('/')
def home():
    return render_template('home.html')

