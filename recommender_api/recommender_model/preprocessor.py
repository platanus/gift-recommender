from gensim.models import KeyedVectors
import numpy as np
from .s3_manager import S3

embeddings = 'embeddings-xs-model.vec'


class Preprocessor(object):
    '''
    Compute a vector representation for the products
    '''
    def __init__(self, embeddings: str = embeddings) -> None:
        S3.ensure_file(embeddings)
        self.vectors = KeyedVectors.load_word2vec_format(embeddings)

    def compute_vector(self, product) -> np.array:
        name_vectors = self.compute_name_vector(product)

        return name_vectors

    def get_vector(self, word: str) -> np.array:
        try:
            return self.vectors.get_vector(word)
        except KeyError:
            return np.zeros(self.vectors.vector_size)

    def compute_name_vector(self, product) -> np.array:
        tokens = product.name.lower().split()
        vectors = np.array([self.get_vector(token) for token in tokens])
        return np.average(vectors, axis=0)


if __name__ == '__main__':
    preprocessor = Preprocessor(embeddings)
    print(preprocessor.get_vector('auto'))
