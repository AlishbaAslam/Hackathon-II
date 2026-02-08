"""AI Agent Service for Todo Management

This module implements an OpenAI Agent with MCP tool integration for natural language processing
of todo management commands.
"""

import json
from typing import Dict, List, Any, Optional
from .openrouter_client import get_openrouter_client
from ..mcp_tools.task_tools import add_task_async as add_task, list_tasks_async as list_tasks, complete_task_async as complete_task, delete_task_async as delete_task, update_task_async as update_task


class AgentService:
    """Service for managing AI agent interactions with task management tools"""

    def __init__(self):
        """Initialize the agent service"""
        self.client = get_openrouter_client()

    async def process_message(
        self,
        user_id: str,
        message_content: str,
        conversation_history: Optional[List[Dict]] = None,
        session=None
    ) -> Dict[str, Any]:
        """
        Process a user message and return AI-generated response with tool calls.
        Prioritizes real tool results over LLM hallucinations.

        Args:
            user_id: ID of the user sending the message
            message_content: Natural language message from the user
            conversation_history: Previous messages in the conversation (optional)

        Returns:
            Dictionary containing response and tool calls
        """
        # First, identify and execute any tool calls based on the user's message
        tool_calls_result = await self._identify_and_execute_tool_calls(
            user_id=user_id,
            message_content=message_content,
            session=session
        )

        # If tool calls were executed successfully, prioritize those results
        if tool_calls_result.get("tool_calls"):
            # Build response based on actual tool results (no hallucination)
            successful_tool_responses = []

            for tool_call in tool_calls_result.get("tool_calls", []):
                if "error" not in tool_call.get("result", {}):
                    result = tool_call["result"]

                    if tool_call["name"] == "add_task":
                        successful_tool_responses.append(f"✅ Added task: {result.get('title', 'Unknown')}")

                    elif tool_call["name"] == "list_tasks":
                        task_list = result if isinstance(result, list) else []
                        # Get the status from the arguments to customize the response
                        requested_status = tool_call["arguments"].get("status", "all")

                        if task_list:
                            # Build numbered list with titles and status using short_id for easy reference
                            task_items = []
                            for idx, task in enumerate(task_list, 1):
                                short_id = task.get('short_id', idx)  # Use enumeration index if short_id not available
                                title = task.get('title', 'Untitled')
                                completed_status = "✓" if task.get('completed', False) else "○"
                                task_items.append(f"{short_id}. [{completed_status}] {title}")

                            # Customize header based on requested status
                            if requested_status == "completed":
                                header = f"Here are your completed tasks ({len(task_list)} total):"
                            elif requested_status == "pending":
                                header = f"Here are your pending tasks ({len(task_list)} total):"
                            else:
                                header = f"Here are your tasks ({len(task_list)} total):"

                            # Combine header with formatted task list
                            formatted_list = header + "\n" + "\n".join(task_items)
                            successful_tool_responses.append(formatted_list)
                        else:
                            # Handle empty list case with appropriate message based on requested status
                            if requested_status == "completed":
                                successful_tool_responses.append("You don't have any completed tasks yet. Keep going! 😊")
                            elif requested_status == "pending":
                                successful_tool_responses.append("You don't have any pending tasks. Great job! 🎉")
                            else:
                                successful_tool_responses.append("You don't have any tasks yet. Want to add one?")

                    elif tool_call["name"] == "complete_task":
                        successful_tool_responses.append(f"✅ Completed task: {result.get('title', 'Unknown')}")

                    elif tool_call["name"] == "delete_task":
                        successful_tool_responses.append(f"🗑️ Deleted task: {result.get('title', 'Unknown')}")

                    elif tool_call["name"] == "update_task":
                        successful_tool_responses.append(f"✏️ Updated task: {result.get('title', 'Unknown')}")

            # If there were successful tool executions, return response based on real data
            if successful_tool_responses:
                combined_response = " " + " ".join(successful_tool_responses)

                return {
                    "response": combined_response,
                    "tool_calls": tool_calls_result.get("tool_calls", []),
                    "tool_results": tool_calls_result.get("results", [])
                }

            # If tool calls had errors, return error messages
            error_tool_responses = []
            for tool_call in tool_calls_result.get("tool_calls", []):
                if "error" in tool_call.get("result", {}):
                    error_msg = tool_call["result"]["error"]
                    error_tool_responses.append(f"❌ Error: {error_msg}")

            if error_tool_responses:
                return {
                    "response": " ".join(error_tool_responses),
                    "tool_calls": tool_calls_result.get("tool_calls", []),
                    "tool_results": tool_calls_result.get("results", [])
                }

        # If no tool calls matched, fall back to LLM response without mentioning tasks
        # Prepare the messages for the AI with a neutral system message
        messages = []

        # Neutral system message that doesn't prompt task hallucination
        system_content = """
You are a helpful assistant. If the user asks about tasks, respond naturally without inventing or hallucinating task data.
If they want to manage tasks, guide them to use the appropriate commands like 'add task', 'list tasks', etc.
Only provide information about tasks if it comes from actual tool results.
"""

        messages.append({
            "role": "system",
            "content": system_content
        })

        # Add conversation history if available
        if conversation_history:
            messages.extend(conversation_history)

        # Add the current user message
        messages.append({
            "role": "user",
            "content": message_content
        })

        try:
            # Get response from the AI model
            response_content = await self.client.chat_completion(messages)

            return {
                "response": response_content,
                "tool_calls": tool_calls_result.get("tool_calls", []),
                "tool_results": tool_calls_result.get("results", [])
            }
        except Exception as e:
            # If there was an error with the LLM but no tool calls were made
            return {
                "response": f"Sorry, I encountered an error processing your request: {str(e)}",
                "tool_calls": [],
                "tool_results": []
            }

    async def _identify_and_execute_tool_calls(
        self,
        user_id: str,
        message_content: str,
        session=None
    ) -> Dict[str, Any]:
        """
        Identify and execute appropriate tool calls based on the message content.
        This function is tool-first and executes real tools BEFORE any LLM response.

        Args:
            user_id: ID of the user
            message_content: The user's message to analyze

        Returns:
            Dictionary containing tool calls and results
        """
        message_lower = message_content.lower().strip()
        tool_calls = []
        results = []

        # Strict keyword mapping for add_task - execute real tool
        add_keywords = [
            "add a task", "create a task", "add task", "create task",
            "add to my list", "remember to", "need to", "have to",
            "make a note to", "remind me to", "don't forget to", "add task:"
        ]
        if any(keyword in message_lower for keyword in add_keywords):
            title = self._extract_task_title(message_content)
            if title:
                try:
                    result = await add_task(user_id=user_id, title=title, session=session)
                    results.append(result)
                    tool_calls.append({
                        "name": "add_task",
                        "arguments": {"user_id": user_id, "title": title},
                        "result": result
                    })
                except Exception as e:
                    results.append({"error": str(e)})
                    tool_calls.append({
                        "name": "add_task",
                        "arguments": {"user_id": user_id, "title": title},
                        "result": {"error": str(e)}
                    })

        # Strict keyword mapping for list_tasks - execute real tool
        elif any(keyword in message_lower for keyword in [
            "show me", "list", "view", "display", "my tasks", "what do i have",
            "what's pending", "show tasks", "what's on my list", "all tasks",
            "list all", "what are my", "tasks list", "see my tasks", "list my tasks",
            "show my tasks", "what tasks do i have", "my task list"
        ]):
            # Determine status filter more accurately with emphasis on specific status indicators
            status = "all"

            # First, check for specific status requests which take priority over general "all" requests
            if any(completed_keyword in message_lower for completed_keyword in [
                "completed", "done", "finished", "completed tasks", "done tasks",
                "what's done", "finished tasks", "show completed", "my completed tasks",
                "what's completed", "all completed tasks", "completed task list"
            ]):
                status = "completed"
            elif any(pending_keyword in message_lower for pending_keyword in [
                "pending", "not done", "to do", "todo", "unfinished", "incomplete",
                "what's left", "what remains", "remaining tasks"
            ]):
                status = "pending"

            try:
                result = await list_tasks(user_id=user_id, status=status, session=session)
                results.append(result)
                tool_calls.append({
                    "name": "list_tasks",
                    "arguments": {"user_id": user_id, "status": status},
                    "result": result
                })
            except Exception as e:
                results.append({"error": str(e)})
                tool_calls.append({
                    "name": "list_tasks",
                    "arguments": {"user_id": user_id, "status": status},
                    "result": {"error": str(e)}
                })

        # Strict keyword mapping for complete_task - execute real tool
        elif any(keyword in message_lower for keyword in [
            "complete", "finish", "done", "mark as complete", "check off",
            "tick off", "complete task", "finish task", "mark done",
            "mark as done", "check task", "cross off", "complete task",
            "finish up", "mark complete"
        ]):
            task_id = self._extract_task_id(message_content)
            if task_id:
                try:
                    result = await complete_task(user_id=user_id, task_id=task_id, session=session)
                    results.append(result)
                    tool_calls.append({
                        "name": "complete_task",
                        "arguments": {"user_id": user_id, "task_id": task_id},
                        "result": result
                    })
                except Exception as e:
                    results.append({"error": str(e)})
                    tool_calls.append({
                        "name": "complete_task",
                        "arguments": {"user_id": user_id, "task_id": task_id},
                        "result": {"error": str(e)}
                    })

        # Strict keyword mapping for delete_task - execute real tool
        elif any(keyword in message_lower for keyword in [
            "delete", "remove", "cancel", "get rid of", "eliminate", "erase",
            "remove task", "delete task", "trash", "dispose", "clear task",
            "get rid of task", "delete the task", "remove the task", "cancel task"
        ]):
            task_id = self._extract_task_id(message_content)
            if task_id:
                try:
                    result = await delete_task(user_id=user_id, task_id=task_id, session=session)
                    results.append(result)
                    tool_calls.append({
                        "name": "delete_task",
                        "arguments": {"user_id": user_id, "task_id": task_id},
                        "result": result
                    })
                except Exception as e:
                    results.append({"error": str(e)})
                    tool_calls.append({
                        "name": "delete_task",
                        "arguments": {"user_id": user_id, "task_id": task_id},
                        "result": {"error": str(e)}
                    })

        # Strict keyword mapping for update_task - execute real tool
        elif any(keyword in message_lower for keyword in [
            "update", "change", "modify", "edit", "rename", "alter",
            "update task", "change task", "modify task", "edit task",
            "rename task", "update title", "change title", "modify title",
            "edit title", "rename title", "update the task", "change the task",
            "update description", "change description", "modify description", "update desc", "change desc"
        ]):
            task_id = self._extract_task_id(message_content)

            # Extract both title and description if possible
            new_title = None
            new_description = None

            # Check if user wants to update description specifically
            if any(desc_keyword in message_lower for desc_keyword in ["description", "desc"]):
                new_description = self._extract_task_description(message_content)

                # If description is missing or invalid, add error message
                if not new_description and any(desc_keyword in message_lower for desc_keyword in ["description", "desc"]):
                    error_msg = "Please provide the new description after 'description :', e.g., 'update task 5 description : new details here'"
                    results.append({"error": error_msg})
                    tool_calls.append({
                        "name": "update_task",
                        "arguments": {"user_id": user_id, "task_id": task_id},
                        "result": {"error": error_msg}
                    })
                    # Don't proceed with the update since we have an error
                    new_title = None
                    new_description = None
                    task_id = None  # This will prevent the update from proceeding

            # Check if user wants to update title specifically (but not if they mentioned description)
            if not new_description and any(title_keyword in message_lower for title_keyword in ["title", "to"]):
                new_title = self._extract_task_title(message_content)
            elif not new_description:  # If no description was extracted, try to extract title
                new_title = self._extract_task_title(message_content)

            # Proceed with update if we have either a task_id and at least one update parameter
            if task_id and (new_title or new_description):
                try:
                    # Call update_task with both parameters (only non-None ones will be used)
                    result = await update_task(user_id=user_id, task_id=task_id, title=new_title, description=new_description, session=session)
                    results.append(result)

                    # Create arguments dict with only the parameters that have values
                    update_args = {"user_id": user_id, "task_id": task_id}
                    if new_title:
                        update_args["title"] = new_title
                    if new_description:
                        update_args["description"] = new_description

                    tool_calls.append({
                        "name": "update_task",
                        "arguments": update_args,
                        "result": result
                    })
                except Exception as e:
                    results.append({"error": str(e)})

                    # Create arguments dict with only the parameters that have values for error case too
                    update_args = {"user_id": user_id, "task_id": task_id}
                    if new_title:
                        update_args["title"] = new_title
                    if new_description:
                        update_args["description"] = new_description

                    tool_calls.append({
                        "name": "update_task",
                        "arguments": update_args,
                        "result": {"error": str(e)}
                    })

        return {
            "tool_calls": tool_calls,
            "results": results
        }

    def _extract_task_title(self, message: str) -> Optional[str]:
        """
        Extract a task title from a user message.

        Args:
            message: The user's message

        Returns:
            Extracted task title or None
        """
        import re

        message_lower = message.lower().strip()

        # Enhanced update patterns to handle various update/rename/change commands
        # Only include patterns that relate to title updates, not description updates
        update_patterns = [
            # Pattern for "update task [id] title [new title]" - handles colon, quotes, extra spaces
            r"update\s+task\s+\d+\s+title\s*[,:]*\s*(.+)$",
            # Pattern for "change task [id] title [new title]" - handles colon, quotes, extra spaces
            r"change\s+task\s+\d+\s+title\s*[,:]*\s*(.+)$",
            # Pattern for "rename task [id] to [new title]" - handles colon, quotes, extra spaces
            r"rename\s+task\s+\d+\s+to\s+[\"':]?\s*(.+)$",
            # Pattern for "update task [id] to [new title]" - handles colon, quotes, extra spaces
            r"update\s+task\s+\d+\s+to\s+[\"':]?\s*(.+)$",
            # Pattern for "change task [id] to [new title]" - handles colon, quotes, extra spaces
            r"change\s+task\s+\d+\s+to\s+[\"':]?\s*(.+)$",
            # General pattern for update/rename/change to [new title]
            r"(?:update|change|rename|modify)\s+.*?\s+to\s+[\"':]?\s*(.+)$",
            # Pattern for commands with colons (e.g., "update task 4: buy groceries")
            r"(?:update|change|rename|modify)\s+task\s+\d+\s*[:]\s*(.+)$",
            # Pattern for commands with quotes (e.g., "update task 4 to 'buy groceries'")
            r"(?:update|change|rename|modify)\s+.*?\s+(?:to|title)\s+['\"](.+?)['\"]",
        ]

        for pattern in update_patterns:
            match = re.search(pattern, message_lower)
            if match:
                title = match.group(1).strip()
                # Remove potential trailing punctuation or extra words
                title = re.sub(r'[.,!?;]+$', '', title).strip()
                # Remove quotes if present (handles both opening and closing quotes)
                title = re.sub(r'^["\'](.+?)["\']$', r'\1', title).strip()
                # Remove remaining trailing quote if not paired
                title = re.sub(r'["\']$', '', title).strip()

                # Remove leading colons, spaces and other punctuation
                title = re.sub(r'^[:\s]+', '', title).strip()

                # Remove any leading command remnants but be careful not to remove legitimate content
                title = re.sub(r'^(?:to|the|a|an)\s+', '', title).strip()

                if title and title not in ["me", "it", "them", "that", "this", "there", "here", "to", "the", "a", "an"]:
                    return title.capitalize()

        # Patterns for extracting task titles for creation (keep existing patterns)
        patterns = [
            r"add a task (?:to |)(.*)",
            r"create a task (?:to |)(.*)",
            r"add task (?:to |)(.*)",
            r"create task (?:to |)(.*)",  # Added to handle "create task clean room"
            r"remember to (.*)",
            r"need to (.*)",
            r"have to (.*)",
            r"add (?:a |)(.*)",
            r"create (?:a |)(.*)"
        ]

        for pattern in patterns:
            match = re.search(pattern, message_lower)
            if match:
                title = match.group(1).strip()
                # Clean up the title - be more specific to avoid removing parts of legitimate words
                title = re.sub(r'\b(?:that|i)\b', '', title).strip()  # Remove 'that' and 'i' when standalone
                # Remove leading articles or pronouns that might be left
                title = re.sub(r'^(?:the|a|an)\s+', '', title).strip()

                # Clean up extra whitespace that might have been left by removals
                title = re.sub(r'\s+', ' ', title).strip()

                # Remove leading colons, spaces and other punctuation
                title = re.sub(r'^[:\s]+', '', title).strip()

                if title:
                    return title.capitalize()

        # If no pattern matched, return the original message as title
        # but only if it seems like a reasonable task (not too long, not containing commands)
        if len(message.split()) <= 10 and not any(cmd in message_lower for cmd in ["list", "show", "delete", "complete", "update", "change", "rename", "modify"]):
            return message.strip()

        # Fallback: ask for clarification if it's an update command but title couldn't be extracted clearly
        if any(update_cmd in message_lower for update_cmd in ["update", "change", "rename", "modify"]) and any(digit in message for digit in "0123456789"):
            return None

        return None

    def _extract_task_description(self, message: str) -> Optional[str]:
        """
        Extract a task description from a user message, specifically for update operations.

        Args:
            message: The user's message

        Returns:
            Extracted task description or None
        """
        import re

        message_lower = message.lower().strip()

        # Patterns to extract description content after "description" keyword
        description_patterns = [
            # Pattern for "update task [id] description [new description]"
            r"(?:update|change|modify)\s+task\s+(\d+)\s+description\s+(.+)$",
            # Pattern for "update task [id] description : [new description]"
            r"(?:update|change|modify)\s+task\s+(\d+)\s+description\s*:\s*(.+)$",
            # Pattern for "update task [id] description to [new description]"
            r"(?:update|change|modify)\s+task\s+(\d+)\s+description\s+to\s+(.+)$",
            # Pattern for "update task [id] description 'quoted text'"
            r"(?:update|change|modify)\s+task\s+(\d+)\s+description\s+['\"](.+?)['\"]",
            # Additional pattern for "change task [id] description [new description]"
            r"(?:change|update|modify)\s+task\s+(\d+)\s+description\s+(?:['\":]\s*|\s*)(.+)$",
        ]

        for pattern in description_patterns:
            match = re.search(pattern, message_lower)
            if match:
                # Extract just the description part (the last captured group)
                description = match.groups()[-1].strip()  # Get the last captured group (the description)

                # Remove potential trailing punctuation or extra words
                description = re.sub(r'[.,!?;]+$', '', description).strip()
                # Remove quotes if present (handles both opening and closing quotes)
                description = re.sub(r'^["\'](.+?)["\']$', r'\1', description).strip()
                # Remove remaining trailing quote if not paired
                description = re.sub(r'["\']$', '', description).strip()

                # Remove leading colons, spaces and other punctuation
                description = re.sub(r'^[:\s]+', '', description).strip()

                # Remove any leading command remnants but be careful not to remove legitimate content
                description = re.sub(r'^(?:to|the|a|an|and)\s+', '', description).strip()

                if description and description not in ["me", "it", "them", "that", "this", "there", "here", "to", "the", "a", "an", "for"]:
                    return description.capitalize()

        # If no specific pattern matched, try to extract content after "description" keyword
        # Look for variations like "description", "description :", "description to", "description '...'"
        desc_match = re.search(r'description\s*(?:[:\s]|to\s)*\s*(.*)$', message_lower)
        if desc_match:
            description = desc_match.group(1).strip()

            # Handle quoted content if present
            if description.startswith("'") or description.startswith('"'):
                quote_char = description[0]
                end_quote_pos = description.find(quote_char, 1)
                if end_quote_pos != -1:
                    description = description[1:end_quote_pos]
                else:
                    # If there's no closing quote, just remove the opening quote
                    description = description[1:]

            if description:
                description = description.strip(" '\"")
                # Remove potential trailing punctuation or extra words
                description = re.sub(r'[.,!?;]+$', '', description).strip()
                # Remove leading colons, spaces and other punctuation
                description = re.sub(r'^[:\s]+', '', description).strip()

                if description and description not in ["me", "it", "them", "that", "this", "there", "here", "to", "the", "a", "an", "for"]:
                    return description.capitalize()

        return None

    def _extract_task_id(self, message: str) -> Optional[str]:
        """
        Extract a task ID from a user message. Can be either a UUID or numeric ID.

        Args:
            message: The user's message

        Returns:
            Extracted task ID or None
        """
        import re

        # First, try to find UUID-like patterns (for UUID IDs)
        uuid_pattern = r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'
        uuid_match = re.search(uuid_pattern, message.lower())
        if uuid_match:
            return uuid_match.group()

        # If no UUID found, try to find numbers (for numeric IDs)
        numbers = re.findall(r'\d+', message)
        if numbers:
            try:
                return numbers[0]  # Return the first number found as string
            except ValueError:
                pass

        return None


# Global instance
agent_service = AgentService()


def get_agent_service() -> AgentService:
    """Get the global agent service instance"""
    return agent_service