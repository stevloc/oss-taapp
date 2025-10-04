from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from mail_client_api import get_client
from message import Message

app = FastAPI()
mail_client = get_client()

class MessageSummary(BaseModel):
    """Message summary response model for GET /messages."""
    
    id: str
    from_: str
    to: str
    date: str
    subject: str


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



@app.delete("/messages/{message_id}")
async def delete_message(message_id: str) -> dict[str, str]:
    """Deletes a single message."""
    try:
        success = mail_client.delete_message(message_id)
        if success:
            return {"detail": f"Message with ID {message_id} deleted successfully."}
        raise HTTPException(status_code=404, detail=f"Message with ID {message_id} not found.")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Message with ID {message_id} not found.") from e


@app.get("/messages")
async def get_messages(max_results: int = 10) -> list[MessageSummary]:
    """Fetch a list of message summaries.
    
    Args:
        max_results: Maximum number of messages to return (default: 10)
        
    Returns:
        List of message summaries with id, from, to, date, and subject
        
    Raises:
        HTTPException: If there's an error fetching messages

    """
    try:
        # Get client instance and fetch messages
        client = get_client()
        messages = client.get_messages(max_results=max_results)
        
        # Convert Message objects to MessageSummary objects
        summaries = []
        for message in messages:
            summary = MessageSummary(
                id=message.id,
                from_=message.from_,
                to=message.to,
                date=message.date,
                subject=message.subject
            )
            summaries.append(summary)
            
        return summaries
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error fetching messages: {e!s}"
        ) from e

@app.post(
    "/messages/{message_id}/mark-as-read",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Marks a message as read",
)
async def mark_as_read(message_id: str) -> None:
    """Thin wrapper: delegate to the existing mail client and return 204 on success.
    """
    try:
        # If your client method is named differently (e.g., mark_message_as_read),
        # just change this one call.
        mail_client.mark_as_read(message_id)
    except KeyError as err:
        raise HTTPException(status_code=404, detail="Message not found") from err
    except PermissionError as err:
        raise HTTPException(status_code=403, detail="Forbidden") from err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to mark as read: {e}") from e

