import pandas as pd
from sqlalchemy import create_engine
import os


class DatasetLoader(object):
    def __init__(self):
        self.cols = ['id', 'name', 'price', 'store_id']
        # DB binding
        DB_URL = os.environ.get('DATABASE_URL')
        if not DB_URL:
            user = os.environ.get('POSTGRES_USER')
            pw = os.environ.get('POSTGRES_PW')
            url = os.environ.get('POSTGRES_URL')
            db = os.environ.get('POSTGRES_DB')
            DB_URL = f'postgresql+psycopg2://{user}:{pw}@{url}/{db}'
        self.engine = create_engine(DB_URL)
        self.data = None

    def fetch_products(self):
        self.data = pd.read_sql_table('products', self.engine, columns=self.cols)
        return self.data

    def save(self, path):
        self.data.to_csv(path, index=False)


if __name__ == '__main__':
    dl = DatasetLoader()
    dl.fetch_products()
    dl.save('recommender_api/datasets/products.csv')
