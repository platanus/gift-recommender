from .preprocessor import Preprocessor
from ..models import Product, ProductAction  # noqa T484
import numpy as np
import heapq


class RecommenderModel(object):
    def __init__(self) -> None:
        self.preproc = Preprocessor()
        self.product_vector: dict = {}

    def load_products(self) -> None:
        for product in Product.get_all():
            self.product_vector[product.id] = self.preproc.compute_vector(product)

    def recommend(self, receiver_id: int, num_recommendations: int,
                  min_price: float = 0.0, max_price: float = float('inf')) -> list:
        receiver_likes = self.get_receiver_likes(receiver_id)
        if len(receiver_likes) == 0:
            return self.default_recommendation(num_recommendations)
        receiver_vector = self.compute_receiver_vector(receiver_likes)
        candidate_products = self.get_candidate_products(receiver_id, min_price, max_price)
        recommended_products = heapq.nlargest(
            num_recommendations, candidate_products,
            key=lambda prod: cosine_similarity(receiver_vector, self.vector_from_product(prod)))
        return [product.id for product in recommended_products]

    def compute_receiver_vector(self, receiver_likes: set) -> np.array:
        liked_products_vectors = np.array(
            [self.vector_from_product_id(product_id) for product_id in receiver_likes])
        return np.average(liked_products_vectors, axis=0)

    def vector_from_product(self, product: Product) -> np.array:
        return self.product_vector.setdefault(product.id, self.preproc.compute_vector(product))

    def vector_from_product_id(self, product_id: int) -> np.array:
        return self.product_vector.setdefault(
            product_id, self.preproc.compute_vector(Product.get(product_id)))

    @staticmethod
    def default_recommendation(num_recommendations: int) -> list:
        products_ids = [product.id for product in Product.query.all()]
        return np.random.choice(products_ids, num_recommendations, replace=False).tolist()

    @staticmethod
    def get_receiver_likes(receiver_id: int) -> set:
        return {product_id[0] for product_id in ProductAction.get_liked(receiver_id)}

    @staticmethod
    def get_candidate_products(receiver_id: int, min_price: float, max_price: float) -> list:
        displayed_products_ids = {
            product_id[0] for product_id in ProductAction.get_displayed(receiver_id)}
        return [
            product for product in Product.get_all() if
            (product.id not in displayed_products_ids) and (min_price <= product.price <= max_price)
        ]


def cosine_similarity(vec1: np.array, vec2: np.array) -> float:
    return np.inner(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
