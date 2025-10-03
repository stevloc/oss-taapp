"""Service client adapter that makes the server feel like a local library."""

from mail_client_adapter.main import ServiceClientAdapter, get_mail_client

__all__ = ["ServiceClientAdapter", "get_mail_client"]