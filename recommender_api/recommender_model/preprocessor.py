from gensim.models import KeyedVectors
import numpy as np
from .s3_manager import S3
from .image_feature_extractor import ImageFeatureExtractor
from ..models import genders, ages  # noqa T484

embeddings = 'embeddings-xs-model.vec'


class Preprocessor(object):
    '''
    Compute a vector representation for the products
    '''
    def __init__(self, embeddings: str = embeddings) -> None:
        S3.ensure_file(embeddings)
        self.vectors = KeyedVectors.load_word2vec_format(embeddings)
        print('Language model loaded!')
        self.img_feature_extractor = ImageFeatureExtractor()

    def compute_vector(self, product) -> np.array:
        name_vector = self.compute_name_vector(product)
        price_vector = self.compute_price_vector(product)
        image_vector = self.compute_image_vector(product)
        gender_vector = self.compute_gender_vector(product)
        age_vector = self.compute_age_vector(product)
        return np.concatenate((name_vector, image_vector, price_vector, gender_vector, age_vector),
                              axis=None)

    def get_vector(self, word: str) -> np.array:
        try:
            return self.vectors.get_vector(word)
        except KeyError:
            return np.zeros(self.vectors.vector_size)

    def compute_name_vector(self, product) -> np.array:
        tokens = product.name.lower().split()
        vectors = np.array([self.get_vector(token) for token in tokens])
        return np.average(vectors, axis=0)

    def compute_image_vector(self, product) -> np.array:
        image = S3.fetch_image(product.get_image_key())
        image_tensor = self.img_feature_extractor.tensor_from_image(image)
        result = self.img_feature_extractor.compute_vector(image_tensor)
        return result

    @staticmethod
    def compute_price_vector(product) -> np.array:
        if product.price is None:
            return np.zeros(1)
        return np.array([product.price])

    @staticmethod
    def compute_gender_vector(product) -> np.array:
        if product.gender is None:
            return np.zeros(2)
        if product.gender == genders['either']:
            return np.ones(2)
        result = np.zeros(2)
        result[product.gender - 1] = 1
        return result

    @staticmethod
    def compute_age_vector(product) -> np.array:
        if product.age is None:
            return np.zeros(3)
        if product.age == ages['any']:
            return np.ones(3)
        result = np.zeros(3)
        result[product.age - 1] = 1
        return result


if __name__ == '__main__':
    preprocessor = Preprocessor(embeddings)
    print(preprocessor.get_vector('auto'))
