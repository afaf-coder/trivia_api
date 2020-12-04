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
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        all_categories = {}
        for category in categories:
            all_categories[category.id] = category.type

        return jsonify({'categories': all_categories}), 200

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
        selection = Question.query.order_by(Question.id).all()
        total_questions = len(selection)
        categories = Category.query.order_by(Category.id).all()

        current_questions = paginate_questions(request, selection)

        if (len(current_questions) == 0):
            abort(404)

        categories_dict = {}
        for category in categories:
            categories_dict[category.id] = category.type

        # return values if there are no errors
        return jsonify({
            'success': True,
            'total_questions': total_questions,
            'categories': categories_dict,
            'questions': current_questions
        }), 200

    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            return jsonify({
                'success': True,
                'message': "Delete Successful"
            }), 200
        except:
            # abort if problem deleting question
            abort(422)

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
    def add_question():
        body = request.get_json()
        question = body.get('question', '')
        answer = body.get('answer', '')
        difficulty = body.get('difficulty','')
        category = body.get('category', '')

        if ((question == '') or (answer == '')
                or (difficulty == '') or (category == '')):
            abort(422)

        try:
            question = Question(
                question=question,
                answer=answer,
                difficulty=difficulty,
                category=category)
            question.insert()

            selection = Question.query.order_by(Question.id).all()
            current_question = paginate_questions(request, selection)
            return jsonify({
                'success': True,
                'message': 'Question successfully created!'
            }), 201
        except:
            abort(422)

        return app

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
        search_term = body.get('searchTerm', None)
        if search_term == None:
            abort(422)
        try:
            selection = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()

            if len(selection) == 0:
                abort(404)

            current_question = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'questions': current_question,
                'total_questions': len(Question.query.all())
            }), 200
        except:
            abort(404)

        return app

    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

    @app.route("/categories/<int:category_id>/questions", methods=['GET'])
    def get_question_per_category(category_id):
        category = Category.query.filter_by(id=category_id).one_or_none()

        if (category is None):
            abort(400)

        selection = Question.query.filter_by(category=category.id).all()
        current_question = paginate_questions(request, selection)
        return jsonify({
            'success': True,
            'questions': current_question,
            'total_questions': len(Question.query.all()),
            'current_category': category.type
        }), 200

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

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()
        previous_questions = body.get('previous_questions')
        quiz_category = body.get('quiz_category')

        if ((quiz_category is None) or (previous_questions is None)):
            abort(400)
        if (quiz_category['id'] == 0):
            questions = Question.query.all()
        else:
            questions = Question.query.filter_by(category=quiz_category['id']).all()
        total = len(questions)

        def get_random_question():
            return questions[random.randrange(0, len(questions), 1)]

        def check_if_used(question):
            used = False
            for q in previous_questions:
                if (q == question.id):
                    used = True
            return used

        question = get_random_question()

        while (check_if_used( question)):
            question = get_random_question()
            if (len(previous_questions) == total):
                return jsonify({
                    'success': True
                })

        return jsonify({
            'success': True,
            'question': question.format()
        }), 200

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "not found"
        }), 404

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
          "success": False,
          "error": 400,
          "message": "bad request"
      }), 400

    return app
