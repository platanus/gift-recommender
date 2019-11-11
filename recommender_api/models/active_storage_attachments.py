from . import db


class ActiveStorageAttachments(db.Model):
    __tablename__ = 'active_storage_attachments'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    record_type = db.Column(db.String(), nullable=False)
    record_id = db.Column(db.BigInteger, db.ForeignKey('products.id'), nullable=False)
    blob_id = db.Column(db.BigInteger, db.ForeignKey('active_storage_blobs.id'), nullable=False)

    @staticmethod
    def get_image_blob_from_product(product_id: int) -> int:
        return ActiveStorageAttachments.query.filter_by(name='image', record_type='Product',
                                                        record_id=product_id).first().blob_id
