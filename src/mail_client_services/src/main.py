from fastapi import FastAPI, HTTPException

from mail_client_api import get_client
from message import Message

app = FastAPI()
mail_client = get_client()

@app.get("/messages/{message_id}")
async def get_message_detail(message_id: str) -> Message:
    """Fetches the full detail of a single message.
    """
    try:
        # Use the injected client to get the message
        return mail_client.get_message(message_id)
    except Exception as e:
        # Raise an exception if the message is not found
        raise HTTPException(status_code=404, detail=f"Message with ID {message_id} not found.") from e
