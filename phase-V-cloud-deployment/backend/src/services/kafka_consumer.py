"""
Kafka consumer for task events using Dapr pub/sub.
"""
import asyncio
import json
import logging
from typing import Callable, Dict, Any
from uuid import UUID

import httpx
from pydantic import ValidationError

from ..core.event_schemas import TaskEvent, EVENT_SCHEMAS, KafkaTopics
from ..core.dapr_client import DaprClient

logger = logging.getLogger(__name__)


class KafkaConsumer:
    """
    Kafka consumer that subscribes to Dapr pub/sub topics to process task events.
    """

    def __init__(self, dapr_http_endpoint: str = "http://localhost:3500"):
        self.dapr_http_endpoint = dapr_http_endpoint
        self.dapr_client = DaprClient(dapr_http_endpoint)
        self.event_handlers: Dict[str, Callable] = {}
        self.is_running = False
        self.consumer_task = None

    def subscribe_to_topic(self, topic: str, handler: Callable):
        """
        Subscribe to a specific topic with a handler function.

        Args:
            topic: Topic name to subscribe to
            handler: Async function to handle events from this topic
        """
        self.event_handlers[topic] = handler
        logger.info(f"Subscribed to topic '{topic}' with handler {handler.__name__}")

    async def start_consuming(self):
        """
        Start consuming messages from subscribed topics.
        Note: In Dapr pub/sub, the runtime handles subscription via annotations.
        This method would be used if we were to implement a custom consumer.
        """
        self.is_running = True
        logger.info("Starting Kafka consumer...")

        # In a real implementation, this would connect to Kafka directly
        # For Dapr, the subscription is handled by Dapr runtime with @app.route decorators
        # This is just a placeholder for the concept

        while self.is_running:
            # This is a placeholder loop - actual Dapr subscription is done via HTTP callbacks
            await asyncio.sleep(1)

    async def stop_consuming(self):
        """Stop consuming messages."""
        self.is_running = False
        if self.consumer_task:
            self.consumer_task.cancel()
        logger.info("Stopped Kafka consumer")

    async def process_event(self, topic: str, event_data: Dict[str, Any]):
        """
        Process an incoming event from a topic.

        Args:
            topic: Topic name where the event originated
            event_data: Raw event data
        """
        try:
            # Validate the event against the appropriate schema
            event_type = event_data.get('event_type')

            if not event_type:
                logger.warning(f"No event_type found in event data: {event_data}")
                return

            # Find the appropriate schema for this event type
            schema_class = EVENT_SCHEMAS.get(event_type)
            if not schema_class:
                logger.warning(f"No schema found for event type: {event_type}")
                return

            # Validate the event data against the schema
            try:
                validated_event = schema_class(**event_data)
            except ValidationError as ve:
                logger.error(f"Event validation failed for {event_type}: {ve}")
                return

            logger.info(f"Processing event {validated_event.event_id} of type {event_type} from topic {topic}")

            # Call the appropriate handler if registered
            handler = self.event_handlers.get(topic)
            if handler:
                try:
                    await handler(validated_event)
                except Exception as e:
                    logger.error(f"Error in event handler for topic {topic}: {str(e)}")
                    # Could implement retry logic or dead letter queue here
            else:
                logger.warning(f"No handler registered for topic: {topic}")

        except Exception as e:
            logger.error(f"Error processing event from topic {topic}: {str(e)}")

    def get_subscription_config(self):
        """
        Get the subscription configuration for Dapr pub/sub.
        This would be used to register routes in FastAPI app.
        """
        return {
            "pubsubname": "kafka-pubsub",
            "topic": "task-events",
            "route": "/events/task-events"
        }


# Global consumer instance
consumer = KafkaConsumer()


# Example event handlers
async def handle_task_created_event(event: TaskEvent):
    """Handle task created events."""
    logger.info(f"Handling task created event: {event.event_id}")
    # Business logic for handling task creation
    # Could trigger notifications, audit logging, etc.


async def handle_task_updated_event(event: TaskEvent):
    """Handle task updated events."""
    logger.info(f"Handling task updated event: {event.event_id}")
    # Business logic for handling task updates
    # Could trigger notifications if important fields changed


async def handle_task_completed_event(event: TaskEvent):
    """Handle task completed events."""
    logger.info(f"Handling task completed event: {event.event_id}")

    # Check if this was a recurring task and generate next occurrence
    # This would be handled by the recurring task service in a real implementation
    task_payload = event.payload.get('task_data', {})
    is_recurring = task_payload.get('is_recurring', False)

    if is_recurring:
        logger.info(f"Task {event.task_id} was recurring, triggering next occurrence generation")


async def handle_task_deleted_event(event: TaskEvent):
    """Handle task deleted events."""
    logger.info(f"Handling task deleted event: {event.event_id}")
    # Business logic for handling task deletion
    # Could clean up related data, cancel reminders, etc.


# Register handlers
consumer.subscribe_to_topic(KafkaTopics.TASK_EVENTS, handle_task_created_event)
consumer.subscribe_to_topic(KafkaTopics.TASK_EVENTS, handle_task_updated_event)
consumer.subscribe_to_topic(KafkaTopics.TASK_EVENTS, handle_task_completed_event)
consumer.subscribe_to_topic(KafkaTopics.TASK_EVENTS, handle_task_deleted_event)


# Alternative implementation for direct HTTP route handling in FastAPI
async def handle_dapr_pubsub_event(topic: str, event_data: Dict[str, Any]):
    """
    Handler for Dapr pub/sub events received via HTTP route.
    This would be called from a FastAPI route like:
    @app.post("/events/task-events")
    async def dapr_event_handler(request: Request):
        event_data = await request.json()
        await handle_dapr_pubsub_event("task-events", event_data)
        return {"status": "ACK"}
    """
    await consumer.process_event(topic, event_data)