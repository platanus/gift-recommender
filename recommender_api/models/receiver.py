from . import db


class Receiver(db.Model):
    __tablename__ = 'receivers'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String())
    # email = db.Column(db.String())
    giver_id = db.Column(db.BigInteger, db.ForeignKey('givers.id'))
    # relation_id = db.Column(db.BigInteger)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    product_actions = db.relationship('ProductAction', backref='product_actions', lazy=True)
