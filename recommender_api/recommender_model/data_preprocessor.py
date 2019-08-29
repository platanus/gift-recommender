import pandas as pd
import re
import es_core_news_md
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler

class Preprocessor(object):
  def __init__(self, dataset_path, text_features, numeric_features):
    with open('../mock_dataset/mock_dataset.csv') as f:
      self.df = pd.read_csv(f)
    self.nlp = es_core_news_md.load()
    self.stemmer = SnowballStemmer('spanish')
    self.text_features = text_features
    self.numeric_features = numeric_features
    self.scaler = {}
    self.model_df = pd.DataFrame()

  def _remove_stopwords_and_lemmatize(self, text_feature):
    doc = self.nlp(text_feature)
    #return ' '.join([self.lemmatize(token) for token in doc if not token.is_stop])
    return ' '.join([self.stemmer.stem(self.lemmatize(token)) for token in doc if not token.is_stop])

  def lemmatize(self, token):
    return token.lemma_

  def tokenize(self, feature):
    self.df[feature] = self.df[feature].apply(self._remove_stopwords_and_lemmatize)

  def standardize(self, feature):
    self.scaler[feature] = StandardScaler()
    scaled_df = self.scaler[feature].fit_transform(self.df[[feature]])
    self.model_df = pd.concat([self.model_df, pd.DataFrame(scaled_df, columns=[feature])], axis=1)

  def preprocess(self):
    vectorizer = {}
    for feature in self.numeric_features:
      #self.model_df = pd.concat([self.model_df, self.df[self.numeric_features]], axis=1)
      self.standardize(feature)
    for feature in self.text_features:
      self.tokenize(feature)
      vectorizer[feature] = TfidfVectorizer(max_df=0.5)
      transformation = pd.DataFrame(vectorizer[feature].fit_transform(self.df[feature]).todense())
      transformation.columns = vectorizer[feature].get_feature_names()
      self.model_df = pd.concat([self.model_df, transformation.add_prefix(f'{feature}_')], axis=1)

  def print_data_head(self):
    print(self.model_df.head())

  def save_model_df(self, path):
    self.model_df.to_csv(path)

if __name__ == '__main__':
  preprocessor = Preprocessor('../mock_dataset/mock_dataset.csv', ['item_name', 'item_description'], ['item_price'])
  preprocessor.preprocess()
  preprocessor.print_data_head()
  preprocessor.save_model_df('recommender_api/recommender_model/item_features.csv')
