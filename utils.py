import os
from typing import Dict
import requests

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


def signup_user(username: str, email: str) -> str:
    response = requests.post(
        f"http://{BASE_URL}/users/signup",
        json={"username": username, "email": email},
    )
    response.raise_for_status()
    return response.json()["user_id"]


def create_new_session(user_id: str, quiz_id: str) -> str:
    response = requests.post(
        f"http://{BASE_URL}/sessions/new",
        json={"user_id": user_id, "quiz_id": quiz_id},
    )
    response.raise_for_status()
    return response.json()["session_id"]


def create_new_quiz(quiz: Dict, user_id: str):
    response = requests.post(
        f"http://{BASE_URL}/quiz/new",
        json={"quiz": quiz, "user_id": user_id},
    )
    response.raise_for_status()
    return response.json()["quiz_id"]
