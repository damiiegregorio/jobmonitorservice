from flask import render_template
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from config import db
import config

app = config.connex_app

app.add_api('swagger.yml')


@app.route('/')
def home():
    return render_template('home.html')


migrate = Migrate(app=app, db=db)
manager = Manager(app=app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
    # app.run(host='localhost', port=5000, debug=True)