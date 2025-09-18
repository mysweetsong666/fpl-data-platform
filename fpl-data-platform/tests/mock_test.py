# tests/test_routes.py

import unittest
from unittest.mock import patch, Mock
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.app import app  

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    @patch('app.requests.get')  
    def test_top_players_api(self, mock_get):
        fake_api_data = {
            "elements": [
                {"id": 1, "first_name": "Erling", "second_name": "Haaland", "total_points": 99, "team": 1},
                {"id": 2, "first_name": "Saka", "second_name": "Bukayo", "total_points": 95, "team": 2}
            ],
            "teams": [
                {"id": 1, "name": "Man City"},
                {"id": 2, "name": "Arsenal"}
            ]
        }

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = fake_api_data
        mock_get.return_value = mock_response

        response = self.app.get('/api/players')

        self.assertEqual(response.status_code, 200)

        self.assertIn(b'Haaland', response.data)
        self.assertIn(b'Saka', response.data)