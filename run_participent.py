import random
from run import main_run
from utils import signup_user
from run_moderator import SESSION_ID

if __name__ == "__main__":

    session_id = SESSION_ID
    rand = str(random.randint(0, 1000))
    user_id = signup_user(username=f"yael-{rand}", email="yael-2@email.com")
    print(f"User ID: {user_id}")

    # user_id = "9f7b806c-dd20-4091-a1a9-d7a9809a9135"

    main_run(session_id, user_id, role="participant")
