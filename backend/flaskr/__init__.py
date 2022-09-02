import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    setup_db(app)

    # TODO:Delete the sample route after completing the TODOs
    
    # Setting up CORS. Allow '*' for origins.
    CORS(app)
    # cors = CORS(app, resources={r"/*": {"origins": "*"}})
   
    # Setting Access-Control-Allow Using the after_request decorator
    @app.after_request
    # CORS Headers 
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def get_categories():
        # An endpoint to handle GET requests for all categories.
        # sort alphabetically using order_by(Category.type)
        # instead of order_by(Category.id)
        categories = Category.query.order_by(Category.type).all()
        # formated_categories = [category.format() for category in categories]
        formated_categories = {category.id:category.type for category in categories}
        return jsonify({
            'success' : True,
            'categories' : formated_categories  
        })

    # An endpoint to handle GET requests for questions,
    @app.route('/questions', methods=['GET']) 
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        
        if len(current_questions) == 0:
            abort(404)

        categories = Category.query.order_by(Category.id).all()
        categories_type = {category.id:category.type for category in categories}
        
        return jsonify({
            'success' : True,
            # This endpoint should return a list of questions,
            'questions' : current_questions,
            # number of total questions
            'total_questions' : Question.query.count(),
            # current category
            'current_category' : None,
            # categories
            'categories' : categories_type
            })

    """
    @TODO:
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.
    
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            print(question)

            if question is None:
                abort(404)
            
            question.delete()
            selection = Question.query.order_by(Question.id).all()
            count = Question.query.count()
            current_questions = paginate_questions(request, selection)
            # if count % QUESTIONS_PER_PAGE == 0:
                # go to home page
                # return print('go the previous page')

            return jsonify({
                'success' : True,
                'deleted' : question_id,
                'question' : current_questions,
                'total_questions' : count
            })
            
        except:
            abort(422)

    """
    @TODO:
    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    # An endpoint to POST a new question,
    @app.route('/questions', methods=["POST"])
    def create_question():

        question = Question(
            question = request.get_json().get('question', None),
            answer = request.get_json().get('answer', None),
            category = request.get_json().get('category', None),
            difficulty = request.get_json().get('difficulty', None)
        )
        categories = Category.query.order_by(Category.type).all()
        formated_categories = {category.id:category.type for category in categories}

        if question is None:
            abort(404)
        
        question.insert()
        return jsonify({
            'success' : True,
            'created' :  question.id,
            'question' : question.format(),
            'categories' : formated_categories
        })

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    
    @app.route('/questions/search', methods=["POST"])
    def search():
        searchTerm = request.get_json().get('searchTerm', None)
        print(searchTerm)

        if searchTerm:
            results = Question.query.filter(
                Question.question.ilike("%{}%".format(searchTerm))
                ).all()
            current_questions = paginate_questions(request, results)
            return jsonify({
                'success' : True,
                'questions' : current_questions,
                'total_questions' :  len(results),
                'current_categories' : None
            })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app

