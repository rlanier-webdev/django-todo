# billing/lago.py
import requests
from django.conf import settings
from .exceptions import LagoAPIError

class LagoClient:
    def __init__(self):
        self.base_url = settings.LAGO_API_URL
        self.headers = {
            "Authorization": f"Bearer {settings.LAGO_API_KEY}",
            "Content-Type": "application/json",
        }

    def create_customer(self, external_id, name):
        response = requests.post(
            f"{self.base_url}/customers",
            headers=self.headers,
            json={
                "customer": {
                    "external_id": external_id,
                    "name": name,
                }
            },
            timeout=settings.LAGO_TIMEOUT,
        )

        if not response.ok:
            raise LagoAPIError(
                "Failed to create Lago customer",
                response=response,
            )

        return response.json()

    def send_event(self, event_name, external_customer_id, idempotency_key=None, properties=None):
        import uuid
        from datetime import datetime

        headers = self.headers.copy()
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key

        # Use idempotency_key as transaction_id if provided, otherwise generate UUID
        transaction_id = idempotency_key if idempotency_key else str(uuid.uuid4())

        response = requests.post(
            f"{self.base_url}/events",
            headers=headers,
            json={
                "event": {
                    "transaction_id": transaction_id,
                    "code": event_name,
                    "external_customer_id": external_customer_id,
                    "timestamp": int(datetime.utcnow().timestamp()),
                    "properties": properties or {},
                }
            },
            timeout=settings.LAGO_TIMEOUT,
        )

        if not response.ok:
            raise LagoAPIError(
                "Failed to send Lago event",
                response=response,
            )

        return response.json()
