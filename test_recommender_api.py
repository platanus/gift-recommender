from recommender_api import create_app
import json
import unittest


class TestApi(unittest.TestCase):
    """Test case for the flask api"""

    def setUp(self) -> None:
        self.app = create_app()
        self.client = self.app.test_client()
        self.user_preferences = {
            'likes': [0, 1, 2],
            'dislikes': [3, 4, 5],
        }

    def _build_path(self, num_recommendations: int) -> str:
        path = f'/recommend/{num_recommendations}?'
        for liked_item in self.user_preferences['likes']:
            path += f'&likes={liked_item}'
        for disliked_item in self.user_preferences['dislikes']:
            path += f'&dislikes={disliked_item}'
        return path

    def _test_n_recommendations(self, n: int) -> None:
        path = self._build_path(n)
        resp = self.client.get(path, content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(json.loads(resp.data)['product_ids']), n)

    def test_no_recommendation(self) -> None:
        self._test_n_recommendations(0)

    def test_single_recommendation(self) -> None:
        self._test_n_recommendations(1)

    def test_multiple_recommendations(self) -> None:
        self._test_n_recommendations(2)


if __name__ == '__main__':
    unittest.main()
