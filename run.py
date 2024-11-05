import asyncio
import os
import websockets
import json
import readline
import aioconsole
from websockets.exceptions import ConnectionClosedOK

# Create a message queue for handling incoming messages
message_queue = asyncio.Queue()
input_queue = asyncio.Queue()

instance_timestamp = 0  # Timer for the quiz - Updated by the server

BASE_URL = os.getenv("BASE_URL")

if not BASE_URL:
    raise ValueError("BASE_URL environment variable not set")


def clear_display():
    """Clear the display using ANSI escape codes."""
    clear_screen = "\033[2J"
    curser_home = "\033[H"
    print(clear_screen + curser_home, end="")


async def handle_user_input():
    """Continuously get user input asynchronously."""
    readline.parse_and_bind("tab: complete")
    while True:
        choice = await aioconsole.ainput("")
        await input_queue.put(choice)


async def send_messages(websocket, role):
    """
    Process messages from the queue and send user choices to the WebSocket server.
    """

    global instance_timestamp

    readline.parse_and_bind("tab: complete")

    menu_ = []
    display_text_ = None
    quiz_data = None
    option_selected = False
    while True:
        # Create tasks for both message and input handling
        message_task = asyncio.create_task(message_queue.get())
        input_task = asyncio.create_task(input_queue.get())

        # Wait for either a new message or user input
        done, pending = await asyncio.wait(
            {message_task, input_task}, return_when=asyncio.FIRST_COMPLETED
        )

        # Cancel pending tasks
        for task in pending:
            task.cancel()

        # Get the completed task
        completed_task = done.pop()
        result = completed_task.result()

        # Handle message from server
        if completed_task is message_task:
            clear_display()

            message = result

            quiz_data = message.get("quiz_data")

            display_text = (
                message.get("moderator_display_text")
                if role == "moderator"
                else message.get("participant_display_text")
            )
            menu = (
                message.get("moderator_menu")
                if role == "moderator"
                else message.get("participant_menu")
            )
            event = (
                message.get("moderator_event")
                if role == "moderator"
                else message.get("participant_event")
            )
            instance_timestamp = message.get("timestamp")

            current_question_end_timestamp = quiz_data.get(
                "current_question_end_timestamp"
            )
            if current_question_end_timestamp:
                print(
                    f"Time remaining: {current_question_end_timestamp - instance_timestamp} seconds"
                )
            if event:
                print(event)
            print(display_text)
            if menu != menu_ or display_text != display_text_:
                menu_ = menu
                display_text_ = display_text
                option_selected = False

            if not option_selected:
                print("Select an option:")
                for idx, option_dict in enumerate(menu, 1):
                    option = option_dict.get("option")
                    print(f"{idx}. {option}")

        # Handle user input
        elif completed_task is input_task:
            choice = result
            if menu_:  # Only process input if we have a menu
                if choice.isdigit() and 1 <= int(choice) <= len(menu_):
                    selected_option_dict = menu_[int(choice) - 1]
                    type = (
                        "participant-choice"
                        if role == "participant"
                        else "moderator-choice"
                    )
                    await websocket.send(
                        json.dumps(
                            {
                                "type": type,
                                "choice": selected_option_dict,
                                "quiz_data": quiz_data,
                            }
                        )
                    )
                    print(
                        f"Sent choice '{selected_option_dict.get("option")}' to the server."
                    )
                    option_selected = True
                elif choice == "q":
                    print("Exiting...")
                    await websocket.close()
                    return
                else:
                    print(
                        "Invalid choice. Please select a valid option or 'q' to quit."
                    )


async def receive_messages(websocket):
    """Continuously receive messages from the WebSocket server."""
    try:
        while True:
            message = await websocket.recv()
            response = json.loads(message)
            await message_queue.put(response)
    except ConnectionClosedOK as e:
        if e.code == 1000:
            print("\nConnection closed normally by server")
    except websockets.exceptions.ConnectionClosed as e:
        print(f"\nConnection closed unexpectedly: code={e.code}, reason={e.reason}")
    except websockets.exceptions.ConnectionClosed as e:
        print(f"\nConnection closed unexpectedly: code={e.code}, reason={e.reason}")


async def test_ws(session_id: str, user_id: str, role: str):
    url = f"ws://{BASE_URL}/{session_id}"
    headers = [("user_id", user_id), ("role", role)]
    try:
        async with websockets.connect(url, extra_headers=headers) as websocket:
            tasks = [
                asyncio.create_task(send_messages(websocket, role)),
                asyncio.create_task(receive_messages(websocket)),
                asyncio.create_task(handle_user_input()),
            ]
            try:
                # Wait for any task to complete (or fail)
                done, pending = await asyncio.wait(
                    tasks, return_when=asyncio.FIRST_COMPLETED
                )

                # Handle completed tasks
                for task in done:
                    try:
                        # Get the result or exception
                        task.result()
                    except websockets.exceptions.ConnectionClosed:
                        print("\nConnection closed by server")
                    except Exception as e:
                        print(f"Task failed with error: {e}")

                # Cancel pending tasks
                for task in pending:
                    task.cancel()
                    try:
                        await task
                    except asyncio.CancelledError:
                        pass  # Expected when cancelling
                    except Exception as e:
                        print(f"Error while cancelling task: {e}")

            except Exception as e:
                print(f"Error in main loop: {e}")
            finally:
                for task in tasks:
                    if not task.done():
                        task.cancel()
                        try:
                            await task
                        except asyncio.CancelledError:
                            pass  # Expected when cancelling
                        except Exception as e:
                            print(f"Error while cleaning up task: {e}")

    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed: {e}")
    except Exception as e:
        print(f"Connection error: {e}")


def main_run(session_id: str, user_id: str, role: str):
    asyncio.run(test_ws(session_id, user_id, role))
