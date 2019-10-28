import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    # CORS(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
    @app.route('/categories')
    def get_categories():
        all_categories = Category.query.all()
        categories = [category.format() for category in all_categories]
        return jsonify({'categories': categories})

    '''
  @TODO:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''

    @app.route('/questions')
    def get_questions():
        page = request.args.get('page', 1, type=int)
        selection = Question.query.order_by(Question.category).all()
        current_questions = paginate_questions(request, selection)
        categories_cur = Category.query.order_by(Category.id).all()
        categories = [category.format() for category in categories_cur]

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(Question.query.all()),
            'current_category': 'dami',
            'categories': categories
        })

    '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''

    '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
    @app.route('/questions', methods=['POST'])
    def create_question():

        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)
        int_difficulty = int(new_difficulty)

        try:
            question = Question(question=new_question, answer=new_answer,
                                category=new_category, difficulty=int_difficulty)
            question.insert()

            return jsonify({
                'success': True,
                'question_id': question.id,
            })

        except:
            abort(422)

    '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()

        search_data = body.get('searchTerm', None)

        try:
            found_questions = Question.query.filter(
                Question.question.ilike('%' + search_data + '%')).all()
            search_data = [question.format() for question in found_questions]

            if len(found_questions) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'questions': search_data,
                'total_questions': len(search_data),
                'current_category': 'many'
            })

        except:
            abort(422)

    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        all_questions = Question.query.filter(
            Question.category == category_id).all()
        questions = [question.format() for question in all_questions]

        if len(questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': len(questions),
            'current_category': category_id,
        })

    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    return app
