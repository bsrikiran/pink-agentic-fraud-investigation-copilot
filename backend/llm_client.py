"""
Purpose: Infrastructure communication abstraction engine for OpenAI Chat API endpoints.
"""

import logging
from openai import OpenAI
from backend.config import OPENAI_API_KEY, OPENAI_MODEL, MAX_RETRIES

logger = logging.getLogger("backend.llm_client")

class LLMClient:
    """Dedicated LLM communication infrastructure client handler layer wrapper."""
    
    def __init__(self) -> None:
        self.client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

    def call_chat_completion(self, system_message: str, user_message: str) -> str:
        """Executes a network request call against designated OpenAI chat platforms with robust parsing."""
        if not self.client:
            raise RuntimeError("OpenAI client uninitialized. Check environmental variables configuration paths.")

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]

        attempts = 0
        while attempts < MAX_RETRIES:
            try:
                logger.info(f"Dispatching API Request to {OPENAI_MODEL} (Attempt {attempts + 1}/{MAX_RETRIES})")
                response = self.client.chat.completions.create(
                    model=OPENAI_MODEL,
                    messages=messages,
                    response_format={"type": "json_object"},
                    temperature=0.0
                )
                
                # Dynamic extraction sequence supporting standard API models and custom/mock testing proxies
                if hasattr(response, "choices") and response.choices:
                    choice = response.choices[0]
                    if hasattr(choice, "message"):
                        return choice.message.content.strip()
                    elif isinstance(choice, dict) and "message" in choice:
                        msg = choice["message"]
                        return msg.get("content", "").strip() if isinstance(msg, dict) else msg.content.strip()
                
                # Fallback check if response behaves directly as a dictionary structure
                if isinstance(response, dict) and "choices" in response:
                    choice = response["choices"][0]
                    return choice["message"]["content"].strip()
                    
                raise ValueError("Could not extract message content text from response payload structure.")
                
            except Exception as e:
                attempts += 1
                logger.warning(f"API attempt execution failed: {str(e)}")
                if attempts >= MAX_RETRIES:
                    raise RuntimeError(f"Downstream interface connection timeout downstream: {str(e)}")
        
        raise RuntimeError("Unexpected end of LLM client transaction.")
