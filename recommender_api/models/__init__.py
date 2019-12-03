from flask_sqlalchemy import SQLAlchemy, BaseQuery  # noqa: F401

db = SQLAlchemy()

from .active_storage_attachments import ActiveStorageAttachments  # noqa: F401
from .active_storage_blobs import ActiveStorageBlob  # noqa: F401
from .giver import Giver  # noqa: F401
from .product_action import ProductAction  # noqa: F401
from .product import Product, genders, ages  # noqa: F401
from .receiver import Receiver  # noqa: F401
from .store import Store  # noqa: F401
