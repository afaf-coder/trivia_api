# Full Stack Trivia API Backend

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

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

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
## API Reference

Getting Started
- Backend Base URL: http://127.0.0.1:5000/
- Frontend Base URL: http://127.0.0.1:3000/
- Authentication: Authentication or API keys are not used in the project yet.

-----------------------------------------
The error codes currently returned are:

400 – bad request
404 – resource not found
422 – unprocessable
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

REVIEW_COMMENT

Endpoints:
```
GET '/categories' 
GET '/questions' 
GET '/categories/int:category_id/questions'
POST '/questions'
POST '/quizzes'
POST '/questions/search' 
DELETE '/questions/int:question_id'
```
------------------------------------

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
```
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```
GET '/questions'
- Returns all object of questions (including pagination (every 10 questions)) list of questions) 
with number of total questions, current category, categories
- Request Arguments: None
```
 {
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": "Leonardo da Vinci",
            "category": 2,
            "difficulty": 3,
            "id": 1,
            "question": "Who drew the Mona Lisa?"
        },
        {
            "answer": " 32 teeth",
            "category": 1,
            "difficulty": 2,
            "id": 2,
            "question": "How many teeth does an adult human have?"
        },
        {
            "answer": "Three",
            "category": 1,
            "difficulty": 3,
            "id": 3,
            "question": "How many hearts do octopuses have?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 6,
            "difficulty": 1,
            "id": 4,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Abu Bakr",
            "category": 4,
            "difficulty": 1,
            "id": 5,
            "question": "Who was the first Caliph after the death of Prophet Muhammad (PBUH)?"
        },
        {
            "answer": "8 minutes",
            "category": 1,
            "difficulty": 2,
            "id": 6,
            "question": "Roughly how long does it take for the sun’s light to reach Earth – 8 minutes, 8 hours or 8 days?"
        },
        {
            "answer": "Basketball",
            "category": 6,
            "difficulty": 5,
            "id": 7,
            "question": "The LA Lakers and New York Knicks play which sport?"
        },
        {
            "answer": "Blue, yellow, black, green and red",
            "category": 6,
            "difficulty": 3,
            "id": 8,
            "question": "What colours are the five Olympic rings?"
        },
        {
            "answer": "Lebanon",
            "category": 3,
            "difficulty": 3,
            "id": 9,
            "question": "What country is Beirut the capital of?"
        },
        {
            "answer": "Warsaw",
            "category": 3,
            "difficulty": 5,
            "id": 10,
            "question": "What is the capital of Poland?"
        }
    ],
    "success": true,
    "total_questions": 10
}



```
GET '/categories/int:category_id/questions'
- Gets questions by category using the id from the url parameter.
- Request Arguments: None
- sample:```curl http://127.0.0.1:5000/categories/2/questions```
```
{
  "current_category": "Art",
  "questions": [
    {
      "answer": "Leonardo da Vinci",
      "category": 2,
      "difficulty": 3,
      "id": 1,
      "question": "Who drew the Mona Lisa?"
    },
  ],
  "success": true,
  "total_questions": 1
}


```
POST '/questions'
- Creates a new question
- Request Arguments: question: (string)the question body,answer:
 (string)the answer, category: (int) the id of category it belongs to, difficulty: (int) level of dificulty
- Returns success message {'message': 'success'}
- sample:```curl http://127.0.0.1:5000/questions -X POST -H "Content-Type:
 application/json" -d '{ "question": "What is the Capital of Saudi Arabia?", 
 "answer": "Riyadh", "difficulty": 3, "category": "3" }'```
```
{
  "message": "Question successfully created!",
  "success": true
}

```
POST '/quizzes'
- Takes the category and previous questions in the request.
- Return random question not in previous questions.
- sample: ``` curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d 
'{"previous_questions": [2, 3], "quiz_category": {"type": "Science", "id": "1"}}'```
```
{
  "question": {
    "answer": "8 minutes",
    "category":  1,
    "difficulty": 2,
    "id": 6,
    "question": "Roughly how long does it take for the sun’s light to reach 
     Earth – 8 minutes, 8 hours or 8 days?"
  },
  "success": true
}

```
POST '/questions/search'
- Fetches questions that matches a term
- Request Arguments: searchTerm [string term to be searched]
- returns questions that has the search substring
- sample:```curl http://127.0.0.1:5000/questions/search -X
 POST -H "Content-Type: application/json" -d '{"searchTerm": "Mona Lisa"}'```
 ```
{
  "questions": [
    {
      "answer": "Leonardo da Vinci",
      "category": 2,
      "difficulty": 3,
      "id": 1,
      "question": "Who drew the Mona Lisa?"
    }
  ],
  "success": true,
  "total_questions": 11
}
```
DELETE '/questions/int:question_id'
- Deletes a question by id form the url parameter.
- sample: ```curl http://127.0.0.1:5000/questions/3 -X DELETE```
```
{
          "success": "True",
          "message": "Delete Successful"
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
##Authors
Afaf ALanazi 