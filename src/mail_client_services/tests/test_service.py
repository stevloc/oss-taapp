from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

# Assuming your FastAPI code is in 'mail_client_service.main'
# You may need to adjust this import path based on your file structure

from mail_client_services.src.main import app, get_mail_client
from unittest.mock import MagicMock

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
    "body": "This is the full body content for the test message.",
    "body": "This is the full body content for the test message.",
}
# Since Message is a Protocol, we cannot instantiate it directly; use a plain Mock or dict
MOCK_MESSAGE = Mock(**MOCK_MESSAGE_DATA)


# We use patch to replace 'mail_client_service.main.get_client' to control the mail_client instance
@patch("mail_client_service.main.get_client")
def test_get_message_detail_success(mock_get_client: Mock) -> None:
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
def test_get_message_detail_not_found(mock_get_client: Mock) -> None:
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


# Additional brief test cases for GET /messages

@patch("mail_client_services.src.main.get_client")
def test_get_messages_large_max_results(mock_get_client: Mock) -> None:
    """Tests GET /messages with large max_results value."""
    mock_mail_client = mock_get_client.return_value
    mock_mail_client.get_messages.return_value = [MOCK_MESSAGE_1]

    response = client.get("/messages?max_results=1000")

    mock_mail_client.get_messages.assert_called_once_with(max_results=1000)
    assert response.status_code == 200
    assert len(response.json()) == 1


@patch("mail_client_services.src.main.get_client")
def test_get_messages_negative_max_results(mock_get_client: Mock) -> None:
    """Tests GET /messages with negative max_results."""
    mock_mail_client = mock_get_client.return_value
    mock_mail_client.get_messages.return_value = []

    response = client.get("/messages?max_results=-5")

    mock_mail_client.get_messages.assert_called_once_with(max_results=-5)
    assert response.status_code == 200


@patch("mail_client_services.src.main.get_client")
def test_get_messages_single_message(mock_get_client: Mock) -> None:
    """Tests GET /messages returning single message."""
    mock_mail_client = mock_get_client.return_value
    mock_mail_client.get_messages.return_value = [MOCK_MESSAGE_1]

    response = client.get("/messages")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == "msg_001"


@patch("mail_client_services.src.main.get_client")
def test_get_messages_timeout_error(mock_get_client: Mock) -> None:
    """Tests GET /messages with timeout error."""
    mock_mail_client = mock_get_client.return_value
    mock_mail_client.get_messages.side_effect = TimeoutError("Request timeout")

    response = client.get("/messages")

    assert response.status_code == 500
    assert "Request timeout" in response.json()["detail"]


@patch("mail_client_services.src.main.get_client")
def test_get_messages_max_results_one(mock_get_client: Mock) -> None:
    """Tests GET /messages with max_results=1."""
    mock_mail_client = mock_get_client.return_value
    mock_mail_client.get_messages.return_value = [MOCK_MESSAGE_1]

    response = client.get("/messages?max_results=1")

    mock_mail_client.get_messages.assert_called_once_with(max_results=1)
    assert response.status_code == 200
    assert len(response.json()) == 1



@patch("mail_client_service.main.get_client")
def test_delete_message_success(mock_get_client: Mock) -> None:
    """Tests that a successful deletion of a message results in a 200 OK response."""
    # 1. Mock client's behaviour
    mock_mail_client = mock_get_client.return_value
    mock_mail_client.delete_message.return_value = None
    mock_mail_client.delete_message.return_value = None

    # 2. Request
    resp = client.delete(f"/messages/{MOCK_MESSAGE_ID}")
    resp = client.delete(f"/messages/{MOCK_MESSAGE_ID}")

    # 3. Assertions
    mock_mail_client.delete_message.assert_called_once_with(MOCK_MESSAGE_ID)
    assert resp.status_code == 200


@patch("mail_client_service.main.get_client")
def test_delete_message_not_found(mock_get_client: Mock) -> None:
    """Tests that attempt to delete a non-existent message resulting in a 404 Response"""
    missing_id = "ajrlejrq09r"  # Non-existent message ID
    missing_id = "ajrlejrq09r"  # Non-existent message ID

    # 1. Mock client's behaviour
    mock_mail_client = mock_get_client.return_value
    mock_mail_client.delete_message.side_effect = Exception("Message not found.")


    # 2. Request
    resp = client.delete(f"/messages/{missing_id}")

    # 3. Assertions
    mock_mail_client.delete_message.assert_called_once_with(missing_id)
    assert resp.status_code == 404
    assert resp.json()["detail"] == f"Message with ID {missing_id} not found."

def test_mark_as_read_returns_204_and_calls_impl():
    mock = MagicMock()
    app.dependency_overrides[get_mail_client] = lambda: mock

    resp = client.post("/messages/abc123/mark-as-read")

    assert resp.status_code == 204
    mock.mark_as_read.assert_called_once_with("abc123")
    app.dependency_overrides.clear()

def test_mark_as_read_404_when_not_found():
    mock = MagicMock()
    mock.mark_as_read.side_effect = KeyError("missing")
    app.dependency_overrides[get_mail_client] = lambda: mock

    resp = client.post("/messages/missing/mark-as-read")

    assert resp.status_code == 404
    assert resp.json()["detail"] == "Message not found"
    app.dependency_overrides.clear()

def test_mark_as_read_403_on_permission_error():
    mock = MagicMock()
    mock.mark_as_read.side_effect = PermissionError("nope")
    app.dependency_overrides[get_mail_client] = lambda: mock

    resp = client.post("/messages/abc/mark-as-read")
    assert resp.status_code == 403
    app.dependency_overrides.clear()
