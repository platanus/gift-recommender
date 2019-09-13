from . import db


class ProductAction(db.Model):
    __tablename__ = 'product_actions'

    id = db.Column(db.BigInteger, primary_key=True)
    receiver_id = db.Column(db.BigInteger, db.ForeignKey('receivers.id'))
    product_id = db.Column(db.BigInteger, db.ForeignKey('products.id'))
    action_type = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
