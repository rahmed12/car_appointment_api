'''
Allows creation of instances of an app
'''

from flask import Flask
from flask_mongoengine import MongoEngine
from subprocess import call


from settings import MONGODB_HOST

db = MongoEngine()

def create_app(**config_overrides):
    app = Flask(__name__)

    # Load config
    app.config.from_pyfile('settings.py')

    # apply overrides for tests
    app.config.update(config_overrides)


    # setup db
    db.init_app(app)

    # import blueprints
    from appt.views import appts_app
    from app_auth.views import app_appauth

    # register blueprints
    app.register_blueprint(appts_app)
    app.register_blueprint(app_appauth)

    return app


# run shell command to update mongodb with some test data
def fixtures(test_db, collection, fixture):
    command = "mongoimport -h %s \
        -d %s \
        -c %s \
        < %s" % (MONGODB_HOST, test_db, collection, fixture)
    call(command,  shell=True)
