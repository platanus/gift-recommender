from flask import Blueprint, current_app, request

bp = Blueprint('recommender_api', __name__)


@bp.route('/recommend/<int:receiver_id>/<int:num_recommendations>', methods=['GET'])  # type: ignore
def recommend(receiver_id: int, num_recommendations: int) -> dict:
    min_price = request.args.get('min_price', 0.0, float)
    max_price = request.args.get('max_price', float('inf'), float)
    min_promoted = request.args.get('min_promoted', 0, int)
    return {'product_ids': current_app.model.recommend(
            receiver_id, num_recommendations, min_promoted, min_price, max_price)}
