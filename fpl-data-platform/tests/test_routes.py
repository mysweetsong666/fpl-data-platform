# tests/test_routes.py

import sys
import os
import werkzeug
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

if not hasattr(werkzeug, '__version__'):
    werkzeug.__version__ = '3.1.3'
import unittest
from src.app import app
import werkzeug

# 🔧 Monkey-patch
if not hasattr(werkzeug, '__version__'):
    werkzeug.__version__ = '3.1.3'

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'FPL Data Analysis Platform', response.data)

    def test_players_api(self):
        response = self.app.get('/api/players')
        self.assertEqual(response.status_code, 200)

    def test_teams_api(self):
        response = self.app.get('/api/teams')
        self.assertEqual(response.status_code, 200)

    def test_fixtures_api(self):
        response = self.app.get('/api/fixtures')
        self.assertEqual(response.status_code, 200)

