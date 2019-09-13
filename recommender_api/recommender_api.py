from flask import (
    Blueprint
)
from .models import db
from .models.product import Product
from .models.product_action import ProductAction

bp = Blueprint('recommender_api', __name__)


@bp.route('/recommend/<int:receiver_id>/<int:num_recommendations>', methods=['GET'])  # type: ignore
def recommend(receiver_id: int, num_recommendations: int) -> dict:

    displayed_products = [id[0] for id in db.session.query(ProductAction.id).filter(
        ProductAction.receiver_id == receiver_id and ProductAction.action_type == 0
    ).all()]

    result = [r.id for r in Product.query.all()
              if r.id not in displayed_products][:num_recommendations]

    return {'product_ids': result}


@bp.route('/recommend/<int:num_recommendations>', methods=['GET'])  # type: ignore
def default_recommendation(num_recommendations: int) -> dict:

    result = [r.id for r in Product.query.all()][:num_recommendations]

    return {'product_ids': result}
