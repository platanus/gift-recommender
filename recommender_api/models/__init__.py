from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .giver import Giver  # noqa: F401
from .receiver import Receiver  # noqa: F401
