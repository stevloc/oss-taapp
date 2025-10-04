import requests
from typing import List, Dict


class MailClientAdapter:
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def get_messages(self) -> list[dict]:
        """Fetch list of message summaries"""
        resp = requests.get(f"{self.base_url}/messages")
        resp.raise_for_status()
        return resp.json()

    def get_message(self, message_id: str) -> bool:
        """Fetch a single message by ID"""
        resp = requests.get(f"{self.base_url}/messages/{message_id}")
        resp.raise_for_status()
        return resp.json()

    def mark_as_read(self, message_id: str) -> bool:
        """Mark a message as read"""
        resp = requests.post(f"{self.base_url}/messages/{message_id}/mark-as-read")
        resp.raise_for_status()
        return resp.json()

    def delete_message(self, message_id: str) -> bool:
        """Delete a message"""
        resp = requests.delete(f"{self.base_url}/messages/{message_id}")
        resp.raise_for_status()
        return resp.json()
