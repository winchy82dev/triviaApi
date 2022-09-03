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

        self.categories = {
            "type": "great one",
        }

        self.question = {
            'question' : 'What\'s the capital of France ?',
            'answer' : 'Paris',
            'category' : 1,
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
        self.client().post('/categories', json=self.categories)
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    #----------------------------------------------------------------------------#
    # Create
    #----------------------------------------------------------------------------#

    # create a entry in category table to make the tests possible
    def test_create_category(self):
        """Test create_category() on success"""
        
        res = self.client().post('/categories', json=self.categories)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created'],1)

    def test_create_category_error(self):
        """Test create_category() on error"""
        
        res = self.client().post('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Unprocessable Entity')

    def test_create_question(self):
        """Test create_question() on success"""
        
        res = self.client().post('/questions', json=self.question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created'],1)
    
    # create a second question, the first one will be deleted with the test
    def test_create_question_two(self):
        """Test create_question() on success"""
        
        res = self.client().post('/questions', json=self.question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created'],3)
    
    # create a third question, for the quizz
    def test_create_question_three(self):
        """Test create_question() on success"""
        
        res = self.client().post('/questions', json=self.question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created'],2)

    def test_create_question_error(self):
        """Test create_question() on error"""
        
        res = self.client().post('/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Unprocessable Entity')
        


    #----------------------------------------------------------------------------#
    # Read
    #----------------------------------------------------------------------------#

    def test_get_categories(self):
        """Test get_categories() on success"""
 
        res = self.client().get('/categories')
        data = json.loads(res.data)

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


    def test_get_questions_in_category(self):
        """Test get_questions_in_category() on success"""
        
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
      
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['current_category'])
        

    def test_get_questions_in_category_error(self):
        """Test get_questions_in_category() on error"""
        
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)
      
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Ressource Not Found')

    # def test_get_questions_in_category_error_out_of_reach(self):
    #     """Test get_questions_in_category() on error"""
        
    #     res = self.client().get('/categories/1/questions?page=100')
    #     data = json.loads(res.data)
      
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'],'Ressource Not Found')


    #----------------------------------------------------------------------------#
    # Quizz
    #----------------------------------------------------------------------------#

    # def test_quizz(self):
    #     """Test play_quizz() on success"""
    #     quizz = {
    #         'quiz_category': {
    #             'id': 1,
    #             'type': 'great one'
    #         },
    #         'previous_questions': [2]
    #     }
    #     res = self.client().post('/quizzes', json=quizz)
    #     data = json.loads(res.data)
      
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data["question"])

    def test_quizz_error(self):
        """Test play_quizz() on error"""
        
        res = self.client().post('/quizzes')
        data = json.loads(res.data)
      
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Bad Request')

    #----------------------------------------------------------------------------#
    # Search
    #----------------------------------------------------------------------------#

    def test_questions_search_with_results(self):
        """Test search() on success"""
     
        res = self.client().post('/questions/search', json={'searchTerm': 'France'})
        data = json.loads(res.data)
      
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["total_questions"],1)
        self.assertTrue(data['questions'])
        

    def test_questions_search_without_results(self):
        """Test search() on error"""
   
        res = self.client().post('/questions/search', json={'searchTerm': 'lol'})
        data = json.loads(res.data)
      
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data["total_questions"],0)
        self.assertEqual(len(data['questions']),0)

    #----------------------------------------------------------------------------#
    # Delete
    #----------------------------------------------------------------------------#

    def test_delete_question(self):
        """Test delete_question() on success"""
        
        res = self.client().delete('/questions/1')
        data = json.loads(res.data)
        
        question = Question.query.filter(Question.id == 1).one_or_none()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'],1)
        self.assertEqual(question,None)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()