from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

# Assuming your FastAPI code is in 'mail_client_service.main'
# You may need to adjust this import path based on your file structure
from mail_client_services.src.main import app

# 1. Initialize the TestClient
client = TestClient(app)

# 2. Define Mock Data
# Create a valid Message object (Pydantic model) for the successful test case
MOCK_MESSAGE_ID = "test_msg_123"
MOCK_MESSAGE_DATA = {
    "id": MOCK_MESSAGE_ID,
    "thread_id": "thread_456",
    "snippet": "Hello, here is a test email.",
    "subject": "Unit Test Subject",
    "sender": "test@example.com",
    "timestamp": 1678886400,
    "is_read": False,
    "body": "This is the full body content for the test message."
}
# Since Message is a Protocol, we cannot instantiate it directly; use a plain Mock or dict
MOCK_MESSAGE = Mock(**MOCK_MESSAGE_DATA)


# We use patch to replace 'mail_client_service.main.get_client' to control the mail_client instance
@patch("mail_client_service.main.get_client")
def test_get_message_detail_success(mock_get_client: Mock)-> None:
    """Tests that a successful call to the client results in a 200 OK response
    with the correct message data.
    """
    # 1. Configure the mock client's behavior
    mock_mail_client = mock_get_client.return_value
    mock_mail_client.get_message.return_value = MOCK_MESSAGE

    # 2. Act: Make the request
    response = client.get(f"/messages/{MOCK_MESSAGE_ID}")

    # 3. Assertions
    # Verify the underlying dependency was called correctly
    mock_mail_client.get_message.assert_called_once_with(MOCK_MESSAGE_ID)
    
    # Verify the HTTP response status code is 200
    assert response.status_code == 200
    
    # Verify the response body matches the mocked Message data
    assert response.json() == MOCK_MESSAGE_DATA

@patch("mail_client_service.main.get_client")
def test_get_message_detail_not_found(mock_get_client: Mock)-> None:
    """Tests that an exception from the client (e.g., message not found)
    is translated to a 404 Not Found response.
    """
    missing_id = "missing_msg_999"
    
    # 1. Configure the mock client to raise an exception
    mock_mail_client = mock_get_client.return_value
    # Use a generic Exception to simulate any failure that your endpoint catches
    mock_mail_client.get_message.side_effect = Exception("No message found with this ID")

    # 2. Act: Make the request
    response = client.get(f"/messages/{missing_id}")

    # 3. Assertions
    mock_mail_client.get_message.assert_called_once_with(missing_id)
    
    # Verify the HTTP response status code is 404
    assert response.status_code == 404
    
    # Verify the response detail matches the expected error message
    expected_detail = f"Message with ID {missing_id} not found."
    assert response.json()["detail"] == expected_detail
    