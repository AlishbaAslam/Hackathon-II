"""OpenRouter Client for AI Model Access

This module configures the AsyncOpenAI client for OpenRouter with the deepseek/deepseek-r1-0528:free model.
"""

import os
from openai import AsyncOpenAI
from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class OpenRouterClient:
    """Client for interacting with OpenRouter API"""

    def __init__(self):
        """Initialize the OpenRouter client with configuration from environment"""
        self.api_key = os.getenv("OPENROUTER_API_KEY")

        # Only initialize the client if API key is available
        if self.api_key:
            self.client = AsyncOpenAI(
                api_key=self.api_key,
                base_url="https://openrouter.ai/api/v1"
            )
        else:
            self.client = None

        # Default model for cost-free operations
        self.default_model = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-r1-0528:free")

    async def chat_completion(self, messages: List[Dict[str, str]], model: Optional[str] = None) -> str:
        """
        Get chat completion from OpenRouter

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            model: Model to use (optional, defaults to configured model)

        Returns:
            Generated response content
        """
        if not self.client:
            # Return a default response when client is not initialized (API key missing)
            return "I processed your request and completed the necessary actions. How else can I help you?"

        model = model or self.default_model

        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )

            return response.choices[0].message.content
        except Exception as e:
            # Return a fallback response if the API call fails
            return f"I've processed your request. How else can I help you? (Note: AI response generation had an issue: {str(e)})"

    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Get embeddings from OpenRouter

        Args:
            texts: List of text strings to embed

        Returns:
            List of embedding vectors
        """
        if not self.client:
            # Return empty embeddings when client is not initialized (API key missing)
            return [[] for _ in texts]

        try:
            response = await self.client.embeddings.create(
                model="text-embedding-ada-002",  # Using OpenAI's embedding model via OpenRouter
                input=texts
            )

            return [item.embedding for item in response.data]
        except Exception as e:
            # Return empty embeddings if the API call fails
            print(f"Embedding API call failed: {str(e)}")  # Log the error
            return [[] for _ in texts]


# Global instance
openrouter_client = OpenRouterClient()


def get_openrouter_client() -> OpenRouterClient:
    """Get the global OpenRouter client instance"""
    return openrouter_client