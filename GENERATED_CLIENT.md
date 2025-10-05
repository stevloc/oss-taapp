# Auto-Generated Client Setup

This document explains how to set up and use the auto-generated client for the mail service.

## Overview

Instead of manually writing HTTP client code, we use `openapi-python-client` to automatically generate a Python client from the FastAPI service's OpenAPI specification.

## Setup Process

### 1. Install Dependencies
```bash
# Install openapi-python-client
pip install openapi-python-client

# Or using uv
uv add --dev openapi-python-client
```

### 2. Generate the Client
```bash
# Run the generation script
python scripts/generate_client.py
```

This script will:
1. Start the FastAPI service temporarily
2. Fetch the OpenAPI spec from `/openapi.json`
3. Generate a Python client using `openapi-python-client`
4. Save the generated client to `src/mail_client_generated/`

### 3. Use the Generated Client
```python
from mail_client_adapter import get_client

# The adapter automatically uses the generated client if available
client = get_client("http://localhost:8000")
messages = client.get_messages(10)
```

## Architecture

```
User Code
    ↓
GeneratedClientAdapter (implements Client interface)
    ↓
Auto-Generated Client (from openapi-python-client)
    ↓
HTTP Requests to FastAPI Service
    ↓
FastAPI Service (mail_client_services)
    ↓
Core Mail Client (mail_client_api + gmail_client_impl)
```

## Benefits

1. **Type Safety**: Generated client has proper type hints
2. **Auto-Sync**: Client stays in sync with API changes
3. **No Manual HTTP Code**: No need to write requests manually
4. **Documentation**: Generated client includes docstrings from OpenAPI spec
5. **Error Handling**: Proper HTTP error handling built-in

## Testing

```bash
# Test the generated client
python test_generated_client.py
```

## Troubleshooting

### Client Not Found Error
```
ImportError: Generated client not found. Please run 'python scripts/generate_client.py' first.
```

**Solution**: Run the generation script:
```bash
python scripts/generate_client.py
```

### Service Not Running Error
```
Failed to fetch OpenAPI spec: Connection refused
```

**Solution**: Make sure the FastAPI service dependencies are available:
```bash
# Install service dependencies
uv sync

# The generation script starts the service automatically
```

### Generation Failed Error
Check that:
1. `openapi-python-client` is installed
2. The FastAPI service starts without errors
3. The OpenAPI spec is valid (visit http://localhost:8000/docs)

## Manual Fallback

If the generated client is not available, the adapter automatically falls back to the manual `ServiceClientAdapter`. This ensures the system works even without generation.