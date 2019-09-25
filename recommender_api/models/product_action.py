from . import db, BaseQuery

action_types = {
    'display': 0,
    'like': 1,
    'dislike': 2
}


class ProductAction(db.Model):
    __tablename__ = 'product_actions'

    id = db.Column(db.BigInteger, primary_key=True)
    receiver_id = db.Column(db.BigInteger, db.ForeignKey('receivers.id'))
    product_id = db.Column(db.BigInteger, db.ForeignKey('products.id'))
    action_type = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    @staticmethod
    def get_displayed(receiver_id: int) -> BaseQuery:
        return (db.session
                .query(ProductAction.product_id)
                .filter(ProductAction.receiver_id == receiver_id)
                .filter(ProductAction.action_type == action_types['display']))

    @staticmethod
    def get_liked(receiver_id: int) -> BaseQuery:
        return (db.session
                .query(ProductAction.product_id)
                .filter(ProductAction.receiver_id == receiver_id)
                .filter(ProductAction.action_type == action_types['like']))
