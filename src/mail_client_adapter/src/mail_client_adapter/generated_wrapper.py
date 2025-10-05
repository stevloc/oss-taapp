"""Wrapper around auto-generated client to implement the Client interface."""

from typing import List, Iterator
from mail_client_api import Client, Message


class GeneratedMessage(Message):
    """Message implementation using data from generated client."""
    
    def __init__(self, data: dict):
        self._data = data
    
    @property
    def id(self) -> str:
        return self._data.get("id", "")
    
    @property
    def from_(self) -> str:
        return self._data.get("from_", "")
    
    @property
    def to(self) -> str:
        return self._data.get("to", "")
    
    @property
    def date(self) -> str:
        return self._data.get("date", "")
    
    @property
    def subject(self) -> str:
        return self._data.get("subject", "")
    
    @property
    def body(self) -> str:
        return self._data.get("body", "")


class GeneratedClientAdapter(Client):
    """Adapter that wraps the auto-generated client to implement Client interface."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize the adapter.
        
        Args:
            base_url: Base URL of the mail service
        """
        self.base_url = base_url
        
        # Import the generated client (will be available after generation)
        try:
            from mail_client_generated import Client as GeneratedClient
            self._client = GeneratedClient(base_url=base_url)
        except ImportError:
            raise ImportError(
                "Generated client not found. Please run 'python scripts/generate_client.py' first."
            )
    
    def get_messages(self, max_results: int = 10) -> Iterator[Message]:
        """Get messages using the generated client."""
        try:
            # Use the generated client's method
            response = self._client.get_messages(max_results=max_results)
            
            # Convert response to Message objects
            messages = []
            for msg_data in response:
                message = GeneratedMessage(msg_data)
                messages.append(message)
            
            return iter(messages)
            
        except Exception as e:
            raise RuntimeError(f"Failed to get messages: {e}")
    
    def get_message(self, message_id: str) -> Message:
        """Get a specific message using the generated client."""
        try:
            # Use the generated client's method
            response = self._client.get_message_detail(message_id=message_id)
            
            # Convert response to Message object
            return GeneratedMessage(response)
            
        except Exception as e:
            raise RuntimeError(f"Failed to get message {message_id}: {e}")
    
    def delete_message(self, message_id: str) -> bool:
        """Delete a message using the generated client."""
        try:
            # Use the generated client's method
            response = self._client.delete_message(message_id=message_id)
            
            # Extract success from response
            return response.get("success", False)
            
        except Exception as e:
            raise RuntimeError(f"Failed to delete message {message_id}: {e}")
    
    def mark_as_read(self, message_id: str) -> bool:
        """Mark a message as read using the generated client."""
        try:
            # Use the generated client's method
            response = self._client.mark_message_as_read(message_id=message_id)
            
            # Extract success from response
            return response.get("success", False)
            
        except Exception as e:
            raise RuntimeError(f"Failed to mark message {message_id} as read: {e}")


def get_generated_client(base_url: str = "http://localhost:8000") -> GeneratedClientAdapter:
    """Factory function to create a generated client adapter.
    
    Args:
        base_url: Base URL of the mail service
        
    Returns:
        GeneratedClientAdapter instance
    """
    return GeneratedClientAdapter(base_url)