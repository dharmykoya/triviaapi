G# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.

## Endpoints

```
GET '/categories'
GET '/questions'
DELETE '/questions/<int:question_id>'
POST '/questions'
POST '/questions?searchTerm='title''
GET '/categories/<int:category_id>/questions'
POST '/quizzes'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
[
{id:'1', type: "Science"}
{id:'2', type: "Art"}
{id:'3', type: "Geography"}
{id:'4', type: "History"}
{id:'5', type: "Entertainment"}
{id:'6', type: "Sports"}
]


GET '/questions'
- Fetches all questions with pagination limit of 10 per page, total number of questions and categories
- Request Arguments: None
- Returns: A list of dictionaries containing questions, categories and total_questions
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    }
  ],
  "current_category": "dami",
  "questions": [
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Lead",
      "category": 1,
      "difficulty": 5,
      "id": 31,
      "question": "Which toxic element present in automobile exhausts?"
    }
  ],
  "success": true,
  "total_questions": 20
}

DELETE '/questions/<int:question_id>'
- Deletes a question
- Request Arguments: question id
- Returns: a dictionary containing the id of the question deleted and status code indicating success or failure
{
  "deleted_id": 5,
  "success": true
}


POST '/questions'
- Creates new question
- Sample request in json
{
	"question": "The most populated country in Africa is?",
	"answer": "Nigeria",
	"difficulty": 4,
	"category": 2
}
- Returns: a dictionary of the question id and status code indicating success or failure
{
  "question_id": 33,
  "success": true
}


POST '/questions/search'
- Fetches all questions containing the search term
- Request Arguments: json object containing searchTerm
{
	"searchTerm": "title"
}
- Returns: A list of dictionaries containing questions, total_questions and status code
{
  "current_category": "many",
  "questions": [
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 1
}

GET '/categories/<int:category_id>/questions'
- Fetches single category questions
- Request Arguments: category_id
- Returns: A list of dictionaries containing the currrent category, questions, total question found and status code
{
  "current_category": 3,
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 3
}


POST '/quizzes'
- Fetches a single question
- Request Arguments: json object containing a list of previous questions id and category
- sample
{
	"previous_questions": [],
	"quiz_category": {
			"type": "Science",
			"id": 1
		}
}
- Returns: a dictionary containing a single random question
{
  "question": {
    "answer": "Alexander Fleming",
    "category": 1,
    "difficulty": 3,
    "id": 21,
    "question": "Who discovered penicillin?"
  }
}

```

## Error response

```
404:
{
    "success": False,
    "error": 404,
    "message": "resource not found"
}

422:
{
    "success": False,
    "error": 422,
    "message": "unprocessable"
}

400:
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
