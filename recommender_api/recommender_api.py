from flask import Blueprint, current_app

bp = Blueprint('recommender_api', __name__)


@bp.route('/recommend/<int:receiver_id>/<int:num_recommendations>', methods=['GET'])  # type: ignore
def recommend(receiver_id: int, num_recommendations: int) -> dict:
    return {'product_ids': current_app.model.recommend(receiver_id, num_recommendations)}


@bp.route('/recommend/<int:num_recommendations>', methods=['GET'])  # type: ignore
def default_recommendation(num_recommendations: int) -> dict:
    return {'product_ids': current_app.model.default_recommendation(num_recommendations)}
