from . import db


class Store(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String())
    has_enough_balance = db.Column(db.Boolean)

    @staticmethod
    def get(store_id: int) -> 'Store':
        return Store.query.get(store_id)
