from . import db


class Giver(db.Model):
    __tablename__ = 'givers'

    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.String())
    region_id = db.Column(db.BigInteger)
    receivers = db.relationship('Receiver', backref='givers', lazy=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
