from . import db


class ActiveStorageBlob(db.Model):
    __tablename__ = 'active_storage_blobs'

    id = db.Column(db.BigInteger, primary_key=True)
    key = db.Column(db.String(), nullable=False)
    filename = db.Column(db.String(), nullable=False)
    content_type = db.Column(db.String())
    _metadata = db.Column('metadata', db.Text())
    byte_size = db.Column(db.BigInteger, nullable=False)
    checksum = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    @staticmethod
    def get(blob_id: int) -> 'ActiveStorageBlob':
        return ActiveStorageBlob.query.get(blob_id)
