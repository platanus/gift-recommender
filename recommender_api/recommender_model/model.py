from .preprocessor import Preprocessor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from ..models import Product, ProductAction, Store  # noqa T484
import numpy as np
import heapq
from .s3_manager import S3
import pickle


class RecommenderModel(object):
    def __init__(self) -> None:
        self.preproc = Preprocessor()
        self.product_vector_index: dict = {}
        self._product_vector: np.array
        self.initial_dimensions: int = 1292
        self.col_transformer = ColumnTransformer(
            [("num_standardize", StandardScaler(), slice(0, 1291)),  # First 1291 dims are numerical
             ("store_category", OneHotEncoder(
                 categories='auto', dtype='int', handle_unknown='ignore'), slice(1291, None))]
        )

    def load_product_vectors(self, filepath: str) -> None:
        vectors = f'{filepath}.npy'
        indeces = f'{filepath}_index.pkl'
        S3.ensure_file(vectors)
        S3.ensure_file(indeces)
        self._product_vector = np.load(filepath)
        with open(indeces) as f:
            self.product_vector_index = pickle.load(f)
        self.col_transformer.fit(self._product_vector)

    def save_vectors(self, filename: str) -> None:
        np.save(f'{filename}.npy', self._product_vector)
        with open(f'{filename}_index.pkl', 'wb') as f:
            pickle.dump(self.product_vector_index, f)

    def load_products(self) -> None:
        products = Product.get_all()
        self._product_vector = np.empty((len(products), self.initial_dimensions))
        for index, product in enumerate(products):
            self._product_vector[index] = self.preproc.compute_vector(product)
            self.product_vector_index[product.id] = index
        self.col_transformer.fit(self._product_vector)

    def get_product_vector(self, product: 'Product') -> np.array:
        if product.id not in self.product_vector_index:
            self.add_product_vector(product)
        return self.col_transformer.transform(
            [self._product_vector[self.product_vector_index[product.id]]])

    def add_product_vector(self, product: 'Product') -> None:
        self.product_vector_index[product.id] = len(self._product_vector)
        vector = self.preproc.compute_vector(product)
        self.col_transformer.named_transformers_['num_standardize'].partial_fit([vector[:-1]])
        self._product_vector = np.append(self._product_vector, [vector], axis=0)

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
        priority_queue: list = []
        for product in candidate_products:
            heapq.heappush(priority_queue,
                           (-cosine_similarity(receiver_vector, self.get_product_vector(product)),
                            not is_product_promoted(product), product.id, product))
        recommended_products: list = []
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
            [self.get_product_vector(Product.get(product_id)) for product_id in receiver_likes])
        return np.average(liked_products_vectors, axis=0)

    @staticmethod
    def default_recommendation(
            num_recommendations: int, min_promoted: int, candidate_products: list) -> list:
        promoted_products_ids, non_promoted_products_ids =\
            split_promoted_products(candidate_products)
        num_promoted = min(num_recommendations, min_promoted, len(promoted_products_ids))
        result: list = []
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
            is_recommendable(product, displayed_products_ids, min_price, max_price)
        ]


def is_recommendable(product: 'Product', displayed_products_ids: set,
                     min_price: float, max_price: float) -> bool:
    return not product.deleted and (product.id not in displayed_products_ids) and\
        (min_price <= product.price <= max_price)


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
