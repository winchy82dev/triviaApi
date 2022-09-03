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
 
    # Setting up CORS. Allow '*' for origins.
    CORS(app)
   
    # Setting Access-Control-Allow Using the after_request decorator
    # CORS Headers
    @app.after_request
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
            'questions' : current_questions, # list of questions
            'total_questions' : Question.query.count(), # number of total questions
            'current_category' : None,  # current category
            'categories' : categories_type # categories
            })

    # An endpoint to DELETE question using a question ID
    @app.route('/questions/<int:question_id>', methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            print(question)

            if question is None:
                abort(404)
            
            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)
            count = len(current_questions)
            # trying to solve this issue (deleting the 11th or 21th or n1th question)
            # recall the same page and not the page before it
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

    # An endpoint to POST a new question,
    @app.route('/questions', methods=["POST"])
    def create_question():
        try:
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
        except:
            abort(422)

    # a POST endpoint to get questions based on a search term
    @app.route('/questions/search', methods=["POST"])
    def search():
        searchTerm = request.get_json().get('searchTerm', None)
        print(searchTerm)

        if searchTerm:
            results = Question.query.filter(
                Question.question.ilike("%{}%".format(searchTerm))
                ).all()
            
            current_questions = paginate_questions(request, results)
            # get an issue here, the pagination doesn't work for results questions
            # it return paginate question not thoses related with the query
            return jsonify({
                'success' : True,
                'questions' : current_questions,
                'total_questions' :  len(results),
                'current_categories' : None
            })

    # an endpoint to get questions based on category.
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_in_category(category_id):

        if category_id >  Category.query.count():
            abort(404)
           
        category = Category.format(Category.query.get(category_id))
        questions = Question.query.filter(
            Question.category == str(category_id)
            ).all()

        questions_in_category = paginate_questions(request, questions)
        
        return jsonify({
            'success' : True,
            'questions' : questions_in_category,
            'total_questions' : len(questions),
            'current_category' : category['type'],
        })

    # a POST endpoint to get questions to play the quiz
    @app.route('/quizzes', methods=["POST"])
    def play_quizz():
        try:
            category = request.get_json().get('quiz_category', None)
            current_category = category['type']
            
            previous_questions = request.get_json().get('previous_questions', None)
            print(current_category)
            print(previous_questions)
            questions= {}
        
        except Exception:
            abort(400)
        
        # pick all questions
        if category['type'] == 'click':
            query = Question.query.filter(
                Question.id.notin_((previous_questions))
                    ).all()
            questions = paginate_questions(request, query)
            print('all questions', questions)
        
        else:
            # pick selected category
            query = Question.query.filter(
                Question.category == category['id']).filter(
                    Question.id.notin_((previous_questions))
                ).all()
            questions = paginate_questions(request, query)
            print('questions not all:', questions)
            
        if questions:
            print('some questions')
            current_question = questions[random.randint(0, len(questions)-1)]
            print(current_question)
        
        else:
            print('no question')
            return jsonify({
                'success': True,
                "question": None
                })

        return jsonify({
            'success': True,
            'question' : current_question
            })

    # some error handlers on client side
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success' : False,
            'error' : 400,
            'message' : 'Bad Request'
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success' : False,
            'error' : 401,
            'message' : 'Unauthorized'
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'success' : False,
            'error' : 403,
            'message' : 'Forbidden'
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success' : False,
            'error' : 404,
            'message' : 'Ressource Not Found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success' : False,
            'error' : 405,
            'message' : 'Method Not Allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success' : False,
            'error' : 422,
            'message' : 'Unprocessable Entity'
        }), 422

    # some error handlers on server side

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success' : False,
            'error' : 500,
            'message' : 'Internal Server Error'
        }), 500

    @app.errorhandler(501)
    def not_implemented(error):
        return jsonify({
            'success' : False,
            'error' : 501,
            'message' : 'Not Implemented'
        }), 501

    @app.errorhandler(502)
    def bad_gateway(error):
        return jsonify({
            'success' : False,
            'error' : 502,
            'message' : 'Bad Gateway'
        }), 502

    @app.errorhandler(503)
    def service_unavailable(error):
        return jsonify({
            'success' : False,
            'error' : 503,
            'message' : 'Service Unavailable'
        }), 503

    @app.errorhandler(504)
    def gateway_timeout(error):
        return jsonify({
            'success' : False,
            'error' : 504,
            'message' : 'Gateway Timeout'
        }), 504

    return app
