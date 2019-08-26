from recommender_api import create_app
import json
import unittest

class TestApi(unittest.TestCase):
  """Test case for the flask api"""

  def setUp(self):
    self.app = create_app()
    self.client = self.app.test_client()
    self.user_preferences = {
      'likes': [0, 1, 2],
      'dislikes': [3, 4, 5],
      }

  def _buildPath(self, num_recommendations):
    path = f'/recommend/{num_recommendations}?'
    for likedItem in self.user_preferences['likes']:
      path += f'&likes={likedItem}'
    for dislikedItem in self.user_preferences['dislikes']:
      path += f'&dislikes={dislikedItem}'
    return path

  def test_get_recommendation(self):
    for num_recommendations in range(0, 8):
      path = self._buildPath(num_recommendations)

      resp = self.client.get(path, content_type='application/json')
      self.assertEqual(resp.status_code, 200)
      self.assertEqual(len(json.loads(resp.data)['product_ids']), num_recommendations)


if __name__ == '__main__':
  unittest.main()
