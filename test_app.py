from app import app
import json
import unittest

class TestApi(unittest.TestCase):
  """Test case for the flask api"""

  def setUp(self):
    self.app = app
    self.client = self.app.test_client()
    self.data = {  # Represents a user
      'likes': [0, 1, 2],
      'dislikes': [3, 4, 5],
      }

  def test_get_recommendation(self):
    for num_recommendations in range(0, 8):
      path = f'/recommend/{num_recommendations}?'
      for likedItem in self.data['likes']:
        path += f'&likes={likedItem}'
      for dislikedItem in self.data['dislikes']:
        path += f'&dislikes={dislikedItem}'
      resp = self.client.get(path, content_type='application/json')
      self.assertEqual(resp.status_code, 200)
      self.assertEqual(len(json.loads(resp.data)['product_ids']), num_recommendations)


if __name__ == '__main__':
  unittest.main()