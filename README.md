# Quiz-App Clients

This repository contains the client code for the Quiz-App project. The Quiz-App project is a quiz application that allows users to create quizzes, participate in quizzes, and moderate quizzes. The client code in this repository allows users to create quizzes, start quiz sessions, and participate in quiz sessions.

The Quiz-App repository can be found [here](https://github.com/yaelkurz/quiz-app)


## Setup

1. Create a virtual environment:
    ```sh
    python -m venv .venv
    ```

2. Activate the virtual environment:
    - On Windows:
        ```sh
        .venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source .venv/bin/activate
        ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```
4. Create a `.env` file in the root directory of the project and add the following environment variables:
    ```sh
    BASE_URL=<quiz app url> e.g. 127.0.0.1:7860
    ```

## Running the Project

### creating a new user
```python
from utils import signup_user

user_id = signup_user(username="yael", email="yael@email.com")
```
### creating a new quiz
```python
from utils import create_quiz

quiz_id = create_quiz(quiz={
    "name": "Fruits and Vegetables",
    "description": "Fruits and Vegetables Quiz",
    "questions": [
        {
            "question": "Which of the following is a fruit?",
            "points": 10,
            "seconds_to_answer": 30,
            "question_type": "multiple_choice",
            "answers": [
                {"answer": "Apple", "correct_answer": True},
                {"answer": "Carrot", "correct_answer": False},
                {"answer": "Potato", "correct_answer": False},
                {"answer": "Cabbage", "correct_answer": False},
            ],
        },
        {
            "question": "Which of the following is a vegetable?",
            "points": 15,
            "seconds_to_answer": 40,
            "question_type": "multiple_choice",
            "answers": [
                {"answer": "Apple", "correct_answer": False},
                {"answer": "Carrot", "correct_answer": True},
                {"answer": "Banana", "correct_answer": False},
                {"answer": "Kiwi", "correct_answer": False},
            ],
        },
        {
            "question": "Which of the following is a root vegetable?",
            "points": 20,
            "seconds_to_answer": 50,
            "question_type": "multiple_choice",
            "answers": [
                {"answer": "Apple", "correct_answer": False},
                {"answer": "Tomato", "correct_answer": False},
                {"answer": "Potato", "correct_answer": True},
                {"answer": "Cabbage", "correct_answer": False},
            ],
        },
    ],
}, user_id=user_id)
```
### starting a new quiz session
```python
from utils import start_quiz_session

session_id = start_quiz_session(quiz_id=quiz_id, user_id=user_id)
```
### Moderation a quiz session
```python
from run import main_run

main_run(session_id, user_id, role="moderator")
```
### Participating in a quiz session

Make sure to start a quiz session that a moderator has started and is currently running

```python
from run import main_run

main_run(session_id, user_id, role="participant")
```
