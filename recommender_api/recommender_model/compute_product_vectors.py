from flask import Flask
import os
from ..models import db
from .model import RecommenderModel

if __name__ == '__main__':
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY') or 'dev_key'
    )

    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        user = os.environ.get('POSTGRES_USER')
        pw = os.environ.get('POSTGRES_PW')
        url = os.environ.get('POSTGRES_URL')
        _db = os.environ.get('POSTGRES_DB')
        db_url = f'postgresql+psycopg2://{user}:{pw}@{url}/{_db}'

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        model = RecommenderModel()
        model.load_products()
        model.save_vectors('product_vectors')
