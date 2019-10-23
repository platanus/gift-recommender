from .preprocessor import Preprocessor
from ..models import Product, ProductAction, Store  # noqa T484
import numpy as np
import heapq


class RecommenderModel(object):
    def __init__(self) -> None:
        self.preproc = Preprocessor()
        self.product_vector: dict = {}

    def load_products(self) -> None:
        for product in Product.get_all():
            self.product_vector[product.id] = self.preproc.compute_vector(product)

    def recommend(self, receiver_id: int, num_recommendations: int, min_promoted: int = 0,
                  min_price: float = 0.0, max_price: float = float('inf')) -> list:
        candidate_products = self.get_candidate_products(receiver_id, min_price, max_price)
        receiver_likes = self.get_receiver_likes(receiver_id)
        if len(receiver_likes) == 0:
            return self.default_recommendation(
                num_recommendations, min_promoted, candidate_products)
        receiver_vector = self.compute_receiver_vector(receiver_likes)
        return self.top_products_with_promoted(
            receiver_vector, candidate_products, num_recommendations, min_promoted)

    def top_products_with_promoted(self, receiver_vector: list, candidate_products: list,
                                   num_recommendations: int, min_promoted: int) -> list:
        priority_queue = []
        for product in candidate_products:
            heapq.heappush(priority_queue,
                           (-cosine_similarity(receiver_vector, self.vector_from_product(product)),
                            not is_product_promoted(product), product.id, product))
        recommended_products = []
        non_promoted_filler_products = []
        while len(priority_queue) and\
                (min_promoted > 0 or len(recommended_products) < num_recommendations):
            product = heapq.heappop(priority_queue)[-1]
            if is_product_promoted(product):
                recommended_products.append(product.id)
                min_promoted -= 1
            elif num_recommendations - len(recommended_products) > min_promoted:
                recommended_products.append(product.id)
            else:
                non_promoted_filler_products.append(product.id)
        missing_products = num_recommendations - len(recommended_products)
        recommended_products.extend(non_promoted_filler_products[:missing_products])
        return recommended_products

    def compute_receiver_vector(self, receiver_likes: set) -> np.array:
        liked_products_vectors = np.array(
            [self.vector_from_product(Product.get(product_id)) for product_id in receiver_likes])
        return np.average(liked_products_vectors, axis=0)

    def vector_from_product(self, product: Product) -> np.array:
        return self.product_vector.setdefault(product.id, self.preproc.compute_vector(product))

    @staticmethod
    def default_recommendation(
            num_recommendations: int, min_promoted: int, candidate_products: list) -> list:
        promoted_products_ids, non_promoted_products_ids =\
            split_promoted_products(candidate_products)
        num_promoted = min(num_recommendations, min_promoted, len(promoted_products_ids))
        result = []
        result.extend(np.random.choice(promoted_products_ids, num_promoted, replace=False).tolist())
        num_non_promoted = min((num_recommendations - num_promoted), len(non_promoted_products_ids))
        result.extend(np.random.choice(
            non_promoted_products_ids, num_non_promoted, replace=False).tolist())
        return result

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


def split_promoted_products(candidate_products: list) -> tuple:
    promoted_products_ids = []
    non_promoted_products_ids = []
    for product in candidate_products:
        if is_product_promoted(product):
            promoted_products_ids.append(product.id)
        else:
            non_promoted_products_ids.append(product.id)
    return promoted_products_ids, non_promoted_products_ids


def cosine_similarity(vec1: np.array, vec2: np.array) -> float:
    return np.inner(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def is_product_promoted(product: 'Product') -> bool:
    return product.promoted and Store.get(product.store_id).has_enough_balance
