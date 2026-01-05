# billing/services.py
import logging
from .lago import LagoClient
from .exceptions import LagoAPIError

logger = logging.getLogger(__name__)

client = LagoClient()


def create_lago_customer_for_user(user):
    external_id = f"user_{user.id}"

    try:
        client.create_customer(
            external_id=external_id,
            name=user.email,
        )
    except LagoAPIError as e:
        logger.error(
            "Lago customer creation failed",
            extra={
                "user_id": user.id,
                "status_code": getattr(e.response, "status_code", None),
                "response": getattr(e.response, "text", None),
            },
        )
        # Do NOT block signup
        return False

    return True


def track_todo_created(todo):
    external_customer_id = f"user_{todo.user.id}"
    idempotency_key = f"todo-created-{todo.id}"

    try:
        client.send_event(
            event_name="todo.created",
            external_customer_id=external_customer_id,
            idempotency_key=idempotency_key,
        )
    except LagoAPIError as e:
        logger.warning(
            "Failed to track todo.created event",
            extra={
                "todo_id": todo.id,
                "user_id": todo.user.id,
                "status_code": getattr(e.response, "status_code", None),
            },
        )
        # Important: app still works even if billing fails
        return False

    return True
