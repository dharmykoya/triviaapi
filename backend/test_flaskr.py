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
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.new_question = {
            'question': 'Who is honored as Father of Modern Chemistry?',
            'answer': 'Antoine Lavoisier',
            'category': 1,
            'difficulty': 5
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
        response = self.client().get('/categories')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['categories'])

    def test_404_if_category_does_not_exist(self):
        response = self.client().get('/categories/4737/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))
        self.assertTrue(len(data['questions']))

    def test_404_if_page_does_not_exist(self):
        response = self.client().get('/questions?page=200')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_question(self):
        response = self.client().post('/questions', json=self.new_question)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question_id'])

    def test_422_if_info_supplied_is_empty(self):
        wrong_question = {
            'question': 'hello?',
            'new_answer': 'dja'
        }
        response = self.client().post('/questions', json=wrong_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")

    def test_get_questions_by_category(self):
        response = self.client().get('/categories/2/questions')

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_search_questions(self):
        response = self.client().post('/questions/search',
                                      json={'searchTerm': 'title'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_422_if_search_term_is_not_provided(self):
        response = self.client().post('/questions/search',
                                      json={'something': 'title'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")

    def test_delete_question(self):
        response = self.client().delete('/questions/6')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], 6)

    def test_404_if_question_not_found_on_delete(self):
        response = self.client().delete('/questions/68573')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_play_quiz(self):
        body = {
            'previous_questions': [],
            'quiz_category': {
                'id': 0
            }
        }
        response = self.client().post('/quizzes', json=body)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['question'])

    def test_play_quiz_with_category(self):
        body = {
            'previous_questions': [],
            'quiz_category': {
                'id': 2
            }
        }
        response = self.client().post('/quizzes', json=body)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']["category"], 2)

    def test_play_quiz_with_previous_questions(self):
        body = {
            'previous_questions': [2, 3],
            'quiz_category': {
                'id': 2
            }
        }
        response = self.client().post('/quizzes', json=body)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']["category"], 2)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
