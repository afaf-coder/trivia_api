import os
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
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgresql', '12345678','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

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

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_request_beyond_valid_page(self):

        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    def test_successful_question_delete(self):
       res = self.client().delete('/questions/2')
       data = json.loads(res.data)

       self.assertEqual(res.status_code, 200)
       self.assertEqual(data['success'], True)
       self.assertEqual(data['message'], 'Delete Successful')

    def test_404_no_question_to_delete(self):
        res = self.client().delete('/questions/4000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'not found')

    def test_create_questions(self):
        json_data = {
            'question': 'test_question',
            'answer': 'test_answer',
            'difficulty': 1,
            'category': 1
        }
        res = self.client().post('/questions', json=json_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Question successfully created!')

    def test_create_question_with_empty_data(self):
        json_data = {
            'question': '',
            'answer': '',
            'difficulty': 1,
            'category': 1,
        }
        res= self.client().post('/questions', json=json_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_search_questions(self):
        json_data = {'searchTerm': 'what'}

        res = self.client().post('/questions/search', json=json_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))

    def test_empty_search_term_response(self):
        json_data = {'searchTerm': '', }


        res = self.client().post('/questions/search', json=json_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_search_term_not_found(self):
        res = self.client().post('/questions',
        json={'searchTerm': 'vfgtttttu'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    def test_get_questions_per_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'],0)
        self.assertEqual(data['current_category'], 'Art')

    def test_invalid_category_id(self):
        res = self.client().get('/categories/12300/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_quizzes(self):
        json_data = {
            'previous_questions': [2, 3],
            'quiz_category': {"type": "'Science'", "id": "1"},
        }
        res = self.client().post('/quizzes', json=json_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_empty_data_to_play_quiz(self):
        json_data = {
            'previous_questions': [],
            'quiz_category': {},
        }
        res = self.client().post('/quizzes', json=json_data)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()