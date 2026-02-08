"""
Dapr client utilities for interacting with Dapr runtime.
"""
import asyncio
import json
import os
from typing import Any, Dict, Optional
from uuid import uuid4
from datetime import datetime

import httpx
from pydantic import BaseModel

from .event_schemas import TaskEvent, KafkaTopics


class DaprClient:
    """
    Client for interacting with Dapr runtime for pub/sub, state management, etc.
    """

    def __init__(self, dapr_http_endpoint: Optional[str] = None):
        # Fix: Use dynamic port from environment variable
        if dapr_http_endpoint is None:
            dapr_http_port = os.getenv("DAPR_HTTP_PORT", "3500")
            dapr_http_endpoint = f"http://localhost:{dapr_http_port}"

        self.dapr_http_endpoint = dapr_http_endpoint
        self.http_client = httpx.AsyncClient(timeout=httpx.Timeout(30.0))

        print(f"[DAPR_CLIENT] Initialized with endpoint: {self.dapr_http_endpoint}")

    async def publish_event(self, topic: str, event: TaskEvent, max_retries: int = 3) -> bool:
        """
        Publish an event to a Kafka topic via Dapr pub/sub with retry logic.

        Args:
            topic: The Kafka topic name
            event: The event to publish
            max_retries: Maximum number of retry attempts (default: 3)

        Returns:
            True if successfully published, False otherwise
        """
        # Fix: Use "pubsub" as default (created by dapr init)
        # The default Redis pubsub component from dapr init is named "pubsub"
        pubsub_name = os.getenv("DAPR_PUBSUB_NAME", "pubsub")

        # Fix: Get dynamic Dapr HTTP port from environment
        dapr_http_port = os.getenv("DAPR_HTTP_PORT", "3500")
        dapr_endpoint = f"http://localhost:{dapr_http_port}"

        url = f"{dapr_endpoint}/v1.0/publish/{pubsub_name}/{topic}"

        print(f"[DAPR] ========== PUBLISH EVENT DEBUG ==========")
        print(f"[DAPR] Using real pubsub name: {pubsub_name}")
        print(f"[DAPR] Dapr HTTP endpoint: {dapr_endpoint} (port from env: {dapr_http_port})")
        print(f"[DAPR] Full publish URL: {url}")
        print(f"[DAPR] Publishing to topic: {topic}")

        # Convert event to dict and handle UUID serialization
        event_dict = event.dict()

        # Fix: Convert UUID fields to strings for JSON serialization
        if 'user_id' in event_dict and event_dict['user_id']:
            event_dict['user_id'] = str(event_dict['user_id'])
        if 'task_id' in event_dict and event_dict['task_id']:
            event_dict['task_id'] = str(event_dict['task_id'])
        if 'timestamp' in event_dict and event_dict['timestamp']:
            event_dict['timestamp'] = event_dict['timestamp'].isoformat()

        # Fix: Convert event_type enum to its string value
        if 'event_type' in event_dict:
            # If it's an enum, get its value; if it's already a string, keep it
            event_type_value = event_dict['event_type']
            if hasattr(event_type_value, 'value'):
                event_dict['event_type'] = event_type_value.value
            else:
                event_dict['event_type'] = str(event_type_value)
            print(f"[DAPR] Event type after conversion: {event_dict['event_type']}")

        print(f"[DAPR] Event payload (serialized): {json.dumps(event_dict, indent=2)}")
        print(f"[DAPR] ==========================================")

        # Retry logic with exponential backoff
        for attempt in range(1, max_retries + 1):
            try:
                print(f"[DAPR] Attempt {attempt}/{max_retries} to publish event")

                response = await self.http_client.post(
                    url,
                    json=event_dict,
                    timeout=10.0
                )

                print(f"[DAPR] Response status: {response.status_code}")
                print(f"[DAPR] Response body: {response.text}")

                if response.status_code in [200, 204]:
                    print(f"[DAPR] ✓ Successfully published event to {topic} on attempt {attempt}")
                    return True
                else:
                    print(f"[DAPR] ✗ Failed to publish event to {topic}: {response.status_code} - {response.text}")

                    # Check for specific errors
                    if "ERR_PUBSUB_NOT_FOUND" in response.text:
                        print(f"[DAPR] ERROR: Pubsub component '{pubsub_name}' not found!")
                        print(f"[DAPR] Troubleshooting:")
                        print(f"[DAPR]   1. Check if Redis is running: redis-cli ping")
                        print(f"[DAPR]   2. Verify components loaded: curl http://localhost:{dapr_http_port}/v1.0/metadata")
                        print(f"[DAPR]   3. Check dapr run uses: --components-path ./dapr/components")
                        print(f"[DAPR]   4. Component file: dapr/components/redis-pubsub.yaml")

                    # If not the last attempt, wait before retrying
                    if attempt < max_retries:
                        wait_time = 2 ** (attempt - 1)  # Exponential backoff: 1s, 2s, 4s
                        print(f"[DAPR] Retrying in {wait_time} seconds...")
                        await asyncio.sleep(wait_time)

            except httpx.TimeoutException as e:
                print(f"[DAPR] ✗ Timeout publishing event to {topic} (attempt {attempt}/{max_retries}): {str(e)}")

                if attempt < max_retries:
                    wait_time = 2 ** (attempt - 1)
                    print(f"[DAPR] Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)

            except httpx.ConnectError as e:
                print(f"[DAPR] ✗ Connection error publishing event to {topic} (attempt {attempt}/{max_retries}): {str(e)}")
                print(f"[DAPR] Make sure Dapr sidecar is running on {dapr_endpoint}")
                print(f"[DAPR] Check DAPR_HTTP_PORT environment variable (current: {dapr_http_port})")
                print(f"[DAPR] Run 'dapr list' to see actual Dapr HTTP port")

                if attempt < max_retries:
                    wait_time = 2 ** (attempt - 1)
                    print(f"[DAPR] Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)

            except Exception as e:
                print(f"[DAPR] ✗ Error publishing event to {topic} (attempt {attempt}/{max_retries}): {str(e)}")
                import traceback
                traceback.print_exc()

                if attempt < max_retries:
                    wait_time = 2 ** (attempt - 1)
                    print(f"[DAPR] Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)

        print(f"[DAPR] ✗ Failed to publish event after {max_retries} attempts")
        return False

    async def save_state(self, store_name: str, key: str, value: Any) -> bool:
        """
        Save state to Dapr state store.

        Args:
            store_name: Name of the state store component
            key: Key for the state
            value: Value to store

        Returns:
            True if successfully saved, False otherwise
        """
        try:
            url = f"{self.dapr_http_endpoint}/v1.0/state/{store_name}"

            state_item = {
                "key": key,
                "value": value
            }

            response = await self.http_client.post(url, json=[state_item])

            if response.status_code == 200:
                return True
            else:
                print(f"Failed to save state: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"Error saving state: {str(e)}")
            return False

    async def get_state(self, store_name: str, key: str) -> Optional[Any]:
        """
        Get state from Dapr state store.

        Args:
            store_name: Name of the state store component
            key: Key for the state

        Returns:
            The stored value or None if not found
        """
        try:
            url = f"{self.dapr_http_endpoint}/v1.0/state/{store_name}/{key}"

            response = await self.http_client.get(url)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None
            else:
                print(f"Failed to get state: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            print(f"Error getting state: {str(e)}")
            return None

    async def invoke_binding(self, binding_name: str, operation: str, data: Any) -> Optional[Dict[str, Any]]:
        """
        Invoke a Dapr binding.

        Args:
            binding_name: Name of the binding component
            operation: Operation to perform (create, get, delete, etc.)
            data: Data to send with the operation

        Returns:
            Response from the binding or None on error
        """
        try:
            url = f"{self.dapr_http_endpoint}/v1.0/bindings/{binding_name}"

            payload = {
                "operation": operation,
                "data": data
            }

            response = await self.http_client.post(url, json=payload)

            if response.status_code in [200, 204]:
                if response.status_code == 200:
                    return response.json()
                else:
                    return {}
            else:
                print(f"Failed to invoke binding {binding_name}: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            print(f"Error invoking binding {binding_name}: {str(e)}")
            return None

    async def get_metadata(self) -> Optional[Dict[str, Any]]:
        """
        Get Dapr runtime metadata.

        Returns:
            Metadata dictionary or None on error
        """
        try:
            url = f"{self.dapr_http_endpoint}/v1.0/metadata"

            response = await self.http_client.get(url)

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to get Dapr metadata: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            print(f"Error getting Dapr metadata: {str(e)}")
            return None

    async def close(self):
        """Close the HTTP client."""
        await self.http_client.aclose()


# Global Dapr client instance
dapr_client = DaprClient()


async def publish_task_event(event_type: str, user_id: str, task_id: str, payload: Dict[str, Any]) -> bool:
    """
    Helper function to publish a task event.

    Args:
        event_type: Type of event (e.g., 'task.created', 'task.updated')
        user_id: ID of the user triggering the event
        task_id: ID of the task involved in the event
        payload: Additional data about the event

    Returns:
        True if successfully published, False otherwise
    """
    event = TaskEvent(
        event_id=str(uuid4()),
        event_type=event_type,
        user_id=user_id,
        task_id=task_id,
        timestamp=datetime.utcnow(),
        payload=payload
    )

    # Publish to the main task events topic
    success = await dapr_client.publish_event(KafkaTopics.TASK_EVENTS, event)

    # Also publish to specific topic if needed
    if event_type == "task.reminder.scheduled":
        await dapr_client.publish_event(KafkaTopics.REMINDERS, event)
    elif event_type.startswith("task."):
        await dapr_client.publish_event(KafkaTopics.TASK_UPDATES, event)

    return success