from flask import (
  Blueprint,
  current_app
)

bp = Blueprint('recommender_api', __name__)


@bp.route('/recommend/<int:num_recommendations>', methods=['GET'])
def recommend(num_recommendations):
    # likes = request.args.getlist('likes', type=int)
    # dislikes = request.args.getlist('dislikes', type=int)

    products = current_app.products

    return {'product_ids': products.sample(num_recommendations).id.tolist()}
