import logging
import uuid
from django.core.management.base import BaseCommand
from billing.lago import LagoClient, LagoAPIError

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Check Lago API connectivity and event submission"

    def handle(self, *args, **kwargs):
        client = LagoClient()

        # 1️⃣ Test API key / connectivity
        try:
            print("✅ Testing Lago API connectivity...")
            response = client.send_event(
                event_name="debug.ping",
                external_customer_id="test_customer_001",
                idempotency_key=str(uuid.uuid4())
            )
            print("Connection OK:", response)
        except LagoAPIError as e:
            print("❌ Failed connectivity test")
            print("Status code:", getattr(e.response, "status_code", None))
            print("Response body:", getattr(e.response, "text", None))
            return

        # 2️⃣ Check if test customer exists
        try:
            print("\n✅ Checking test customer existence...")
            response = client.create_customer(
                external_id="test_customer_001",
                name="Debug Customer"
            )
            print("Customer exists or created:", response)
        except LagoAPIError as e:
            print("❌ Customer creation failed")
            print("Status code:", getattr(e.response, "status_code", None))
            print("Response body:", getattr(e.response, "text", None))
            return

        # 3️⃣ Send a fake todo.created event
        try:
            print("\n✅ Sending a fake todo.created event...")
            response = client.send_event(
                event_name="todo.created",
                external_customer_id="test_customer_001",
                idempotency_key=str(uuid.uuid4())
            )
            print("Event submitted successfully:", response)
        except LagoAPIError as e:
            print("❌ Event submission failed")
            print("Status code:", getattr(e.response, "status_code", None))
            print("Response body:", getattr(e.response, "text", None))
            return

        print("\n🎉 All Lago checks passed!")
