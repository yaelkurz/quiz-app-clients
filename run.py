import asyncio
import os
import websockets
import json
import readline
import aioconsole

# Create a message queue for handling incoming messages
message_queue = asyncio.Queue()
input_queue = asyncio.Queue()

WEBSOCKET_TIMEOUT = os.getenv("WEBSOCKET_TIMEOUT", 360)


async def handle_user_input():
    """Continuously get user input asynchronously."""
    readline.parse_and_bind("tab: complete")
    while True:
        choice = await aioconsole.ainput("")
        await input_queue.put(choice)


async def send_messages(websocket, role):
    """Process messages from the queue and send user choices to the WebSocket server."""
    readline.parse_and_bind("tab: complete")
    new = True
    menu_ = []
    display_text_ = ""
    timestamp_ = None
    event_ = None

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
            message = result
            if message.get("type") == "heartbeat":
                continue

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
            timestamp = message.get("timestamp")

            if (
                display_text != display_text_
                or menu != menu_
                or event_ != event
                or timestamp_ != timestamp
            ):
                new = True
                menu_ = menu
                display_text_ = display_text
                event_ = event
                timestamp_ = timestamp

                if new:
                    print("\n\n")
                    print(f"\n{timestamp} - {event if event else ''}")
                    print(display_text)
                    print("Select an option:")
                    for idx, option in enumerate(menu, 1):
                        print(f"{idx}. {option}")

        # Handle user input
        elif completed_task is input_task:
            choice = result
            if menu_:  # Only process input if we have a menu
                if choice.isdigit() and 1 <= int(choice) <= len(menu_):
                    selected_option = menu_[int(choice) - 1]
                    type = (
                        "participant-choice"
                        if role == "participant"
                        else "moderator-choice"
                    )
                    await websocket.send(
                        json.dumps({"type": type, "choice": selected_option})
                    )
                    print(f"Sent choice '{selected_option}' to the server.")
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
    while True:
        message = await websocket.recv()
        response = json.loads(message)
        await message_queue.put(response)


async def test_ws(session_id: str, user_id: str, role: str):
    url = f"ws://127.0.0.1:7860/{session_id}"
    headers = [("user_id", user_id), ("role", role)]
    websocket_kwargs = {
        "extra_headers": headers,
        "ping_interval": 20,
        "ping_timeout": 20,
        "close_timeout": 20,
        "max_size": 10 * 1024 * 1024,
        "timeout": WEBSOCKET_TIMEOUT,
    }

    async with websockets.connect(url, **websocket_kwargs) as websocket:
        await asyncio.gather(
            send_messages(websocket, role),
            receive_messages(websocket),
            handle_user_input(),
        )


def main_run(session_id: str, user_id: str, role: str):
    asyncio.run(test_ws(session_id, user_id, role))
