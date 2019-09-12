from . import db


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String())
    price = db.Column(db.Float)
    clicks = db.Column(db.Integer)
    link = db.Column(db.String())
    # clicks_cost = db.Column(db.Float)
    store_id = db.Column(db.BigInteger, db.ForeignKey('stores.id'))
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    # promoted = db.Column(db.Boolean)
