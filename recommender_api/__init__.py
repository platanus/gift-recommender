from flask import Flask
import os

def create_app():
  app = Flask(__name__)
  app.config.from_mapping(
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_key'
  )

  from . import recommender_api
  app.register_blueprint(recommender_api.bp)

  return app