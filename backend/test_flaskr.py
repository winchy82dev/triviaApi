import os
from queue import Empty
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://{}:{}@{}/{}'.format('postgres','lol','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question' : 'What\'s the capital of Frace ?',
            'answer' : 'Paris',
            'category' : 3,
            'difficulty' : 1
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        """Test get_categories() on success"""
        # make a call using a client to a given endpoint
        res = self.client().get('/categories')
        data = json.loads(res.data)
        # make sure that the status code of response is equal to:
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
       
    def test_get_categories_error(self):
        """Test get_categories() on error"""
        res = self.client().get('/categories/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Ressource Not Found')


    def test_get_paginated_questions(self):
        """Test get_questions() on success"""
        
        res = self.client().get('/questions')
        data = json.loads(res.data)
      
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], None)
        self.assertTrue(data['categories'])

    def test_get_paginated_questions_error(self):
        """Test get_questions() on error"""
        
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)
      
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Ressource Not Found')

    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()