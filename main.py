from flask import Flask, render_template
import os
from flask_restful import Resource, Api
from application.config import LocalDevelopmentConfig
from application.database import db
from application.models import User, Decks, Role
from flask_security import Security, SQLAlchemySessionUserDatastore, SQLAlchemyUserDatastore
from application.custom_forms import ExtendedRegisterForm, CustomLoginForm
from application import workers
from flask_caching import Cache

app = None
api = None
celery = None
cache = None

def create_app():

	app = Flask(__name__, template_folder='templates') # Initializing

	# Checking whether the environment is set up for development
	print(os.getenv('ENV', "development"))
	if os.getenv('ENV', "development") == "production":
		raise Exception("Currently no production config is setup.")

	elif os.getenv('ENV', "development") == "stage":
		print("Staring  stage")
		app.config.from_object(StageConfig)
		print("pushed config")

	else:
		print("Staring Local Development")
		app.config.from_object(LocalDevelopmentConfig)
		print("pushed config")

	db.init_app(app)
	api = Api(app)
	app.app_context().push()

	celery = workers.celery

	# Update with configuration
	celery.conf.update(
		broker_url = app.config["CELERY_BROKER_URL"],
		result_backend = app.config["CELERY_RESULT_BACKEND"]
    )

	celery.Task = workers.ContextTask
	app.app_context().push()

	user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
	security = Security(app, user_datastore, register_form=ExtendedRegisterForm, login_form=CustomLoginForm)

	cache = Cache(app)
	app.app_context().push()

	return app, api, celery, cache

app, api, celery, cache = create_app()
from application.controllers import * # Importing all the controllers

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

from application.user_api import UserAPI
api.add_resource(UserAPI, '/api/users/<string:username>', '/api/users')

from application.deck_api import DeckAPI
api.add_resource(DeckAPI,'/api/decks/<string:username>', '/api/decks')

from application.card_api import CardAPI
api.add_resource(CardAPI, '/api/cards/<int:card_id>', '/api/cards')

if __name__ == '__main__':

	# Running the Flask app
	app.run(debug=True)
