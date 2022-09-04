# Backend - Trivia API

This is a simple quiz game, users will be presented with various questions in differents categories.
When the user submits his guess, it will show the correct answer, and gets a point if he answers correctly.

## Setting up the Backend

You can follow along or watch the video for setting up the project locally.

[![Setting Up the trivia App](https://img.youtube.com/vi/iF4INBCVDnE/0.jpg)](https://www.youtube.com/watch?v=iF4INBCVDnE)

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

```bash
pip install virtualenv
python -m virtualenv env
```


3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and run:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database for the application, and `trivia_test` for testing purposes:

```bash
createdb trivia
createdb trivia_test
```

Populate the databases using the `trivia.psql` file provided. From the `backend` directory, run:

```bash
psql trivia < trivia.psql
psql trivia_test < trivia.psql
```
If you get error, you can use those commands instead:

```bash
psql -h localhost -U postgres -d trivia -f trivia.psql
psql -h localhost -U postgres -d trivia_test -f trivia.psql
```

### Run the Server

From the `/backend` directory, first ensure taht you are working on a virtual environment, activate it by running:

```bash
source env/Script/activate
```

You can desactivate your virtual environment at any moment using the following command:

```bash
deactivate
```

To run the server:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting up the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Update: `FLASK_ENV=development` is deprecated, you can use this commands instead:

```bash
export FLASK_APP=flaskr
export FLASK_DEBUG=true
flask run
```

### Link your project to a GitHub repository
First, create a `.gitignore` file and copy the following to it:

```
.vscode
__pycache__
env

# OS generated files #
######################
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
env/
frontend/node_modules/
```

On your main directory initialise your git instance, and make your first commit:

```bash
git init
git add .
git commit -m "first commit"
```

Create a repository on your GitHub account, then run the following:

```bash
git remote add origin <your repo link>
git branch -M main
git push -u origin main
```


## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## API

You can find a detailed documentation of the API endpoints including the URL, request parameters, and the response body.

# API Documentation 

### GET '/categories'

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with the key, `categories`, that contains an object of `id: category_string` key: value pairs, and a second key `success` that contains a boolean `true` for success and `false` for error.

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

### GET '/questions?page=${integer}'

- Fetches a dictionary of questions for all the categories, each page contain 10 questions
- Request Arguments: (optional) `page`, it accepts a `integer` value
- Returns: An object with 10 paginated `questions`, the `total questions` in the db, An object with all the available `categories`, and the `current category`.
- Example response:

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports",
    "7": "anything"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": "5",
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
....
....
    {
      "answer": "The Palace of Versailles",
      "category": "3",
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```

### GET '/categories/${id}/questions'

- Fetches a dictionary of questions related to a specified category `${id}`
- Request Arguments: (required) `id` of a given category, it accepts a `integer` value
- Returns: An object with `questions` for the specified category, the `current category`, and the `total questions` in that category
- Example response:

```json
{
  "current_category": "Science",
  "questions": [
    {
      "answer": "The Liver",
      "category": "1",
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
...
    {
      "answer": "Blood",
      "category": "1",
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

### POST '/questions'

- Send a post request to create a new question
- Request body:

```json
{
    'question' : 'What\'s the capital of France ?',
    'answer' : 'Paris',
    'category' : 3,
    'difficulty' : 1
}
```

- Returns: An object with the created `question` object, the list of available `categories`, and the id of the `created` question
- Example response:

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports",
    "7": "anything"
  },
  "created": 25,
  "question": {
    "answer": "Paris",
    "category": "3",
    "difficulty": 1,
    "id": 25,
    "question": "What is the capital of France ?"
  },
  "success": true
}
```

### POST '/questions/search'

- Send a post request in order to search a specific question by `searchTerm`
- Request body:

```json
{
    'searchTerm' : 'France'
}
```
- Returns: An object with a list of `questions` that contains that `searchTerm`, and their count `total questions`
- Example response:

```json
{
  "current_category": null,
  "questions": [
    {
      "answer": "Paris",
      "category": "3",
      "difficulty": 1,
      "id": 25,
      "question": "What is the capital of France ?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

### POST '/quizzes'

- Send a post request in order to get the next question, the request sends the `quizz category` and an array that contain the `previous_questions` that are already been answered.
- Request body:

```json
{
    'quiz_category':{
        'type':'Geography',
        'id':'3'
    },
    'previous_questions':[]
}
```

- Returns: An object with the current `question` to show on the page
- Example response:

```json
{
  "question": {
    "answer": "Paris",
    "category": "3",
    "difficulty": 1,
    "id": 29,
    "question": "What is the capital of France ?"
  },
  "success": true
}
```

### DELETE '/questions/${id}'

- Deletes a `question` according to its `id` 
- Request Arguments: (required) `id` of a given question, it accepts a `integer` value
- Returns: An object with `deleted` id of the question, and the total remaining questions `total questions`
- Example response:

```json
{
  "deleted": 25,
  "success": true,
  "total_questions": 16
}
```

## Testing

You can run the test by running the `test_flaskr.py` file on your `/backend `directory:

```bash
python test_flaskr.py
```
