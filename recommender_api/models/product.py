from . import db, ActiveStorageAttachments, ActiveStorageBlob


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String())
    price = db.Column(db.Float)
    clicks = db.Column(db.Integer)
    link = db.Column(db.String())
    store_id = db.Column(db.BigInteger, db.ForeignKey('stores.id'))
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    promoted = db.Column(db.Boolean)
    deleted = db.Column(db.Boolean)
    attachments = db.relationship('ActiveStorageAttachments', backref='product', lazy=True)
    display = db.Column(db.Boolean)

    @staticmethod
    def get_all() -> list:
        return Product.query.all()

    @staticmethod
    def get(product_id: int) -> 'Product':
        return Product.query.get(product_id)

    def get_image_key(self) -> str:
        blob_id = ActiveStorageAttachments.get_image_blob_from_product(self.id)
        return ActiveStorageBlob.get(blob_id).key
