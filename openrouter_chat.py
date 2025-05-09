import os
from openai import OpenAI
from typing import List
from langchain.chat_models.base import BaseChatModel
from langchain.schema import BaseMessage, AIMessage
from pydantic import PrivateAttr

class OpenRouterChat(BaseChatModel):
    _client: OpenAI = PrivateAttr()

    def __init__(self, api_key='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', base_url=None, **kwargs):
        super().__init__(**kwargs)
        api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        base_url = base_url or "https://openrouter.ai/api/v1"

        if not api_key:
            raise ValueError("❌ OpenRouter API key not provided or found in env.")

        self._client = OpenAI(api_key=api_key, base_url=base_url)

    def _convert_message(self, message: BaseMessage) -> dict:
        role = getattr(message, "type", "user")
        if role not in ["user", "assistant", "system"]:
            role = "user"  # fallback default
        return {"role": role, "content": message}

    def _generate(self, messages: BaseMessage, stop=None) -> AIMessage:
        formatted_messages = [self._convert_message(messages)]#[self._convert_message(msg) for msg in messages]
        print("DEBUG: Formatted Messages:", formatted_messages)
        try:
            completion = self._client.chat.completions.create(
                model="openai/gpt-3.5-turbo-0613",
                messages=formatted_messages,
                extra_headers={
                    "HTTP-Referer": "https://your-site.com",
                    "X-Title": "RAG Agent Assistant",
                },
                extra_body={}
            )
        except Exception as e:
            raise RuntimeError(f"❌ Request to OpenRouter failed: {e}")

        if not completion or not completion.choices:
            raise ValueError("❌ No choices returned from OpenRouter")

        # You can inspect the full response if needed
        # print("DEBUG: Full Completion Response:", completion)
        #print(completion)
        return completion.choices[0].message.content

    def _call(self, messages: List[BaseMessage], **kwargs) -> AIMessage:
        return self._generate(messages)

    @property
    def _llm_type(self) -> str:
        return "openrouter-chat"
