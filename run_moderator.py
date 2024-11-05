from run import main_run
from utils import signup_user, create_new_session, create_new_quiz

SESSION_ID = "4979dda2-ab8f-4aff-89d7-52b484f979c5"  # Paste session id after creating a new session (for run_participant.py)

NEW_QUIZ = {
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
}
if __name__ == "__main__":

    # user_id = signup_user(username="yael", email="yael@email.com")
    # print(f"User ID: {user_id}")

    user_id = "9abf896d-bc72-441a-928c-e351c81aa09e"

    # quiz_id = create_new_quiz(NEW_QUIZ, user_id)
    # print(f"Quiz ID: {quiz_id}")

    quiz_id = "d5e9858f-d29a-4afe-89e5-393d24f29ba7"

    # session_id = create_new_session(user_id, quiz_id)
    # print(f"Session ID: {session_id}")

    session_id = SESSION_ID

    main_run(session_id, user_id, role="moderator")
