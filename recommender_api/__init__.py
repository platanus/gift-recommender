from flask import Flask
import os
from .data_loader import DatasetLoader


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY') or 'dev_key'
        )

    # Get all data at startup
    data_loader = DatasetLoader()
    app.products = data_loader.fetch_products()
    # dl.save('recommender_api/datasets/products.csv')

    from . import recommender_api
    app.register_blueprint(recommender_api.bp)

    return app
