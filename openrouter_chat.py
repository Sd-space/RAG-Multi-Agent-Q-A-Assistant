import os
import requests
from typing import List
from langchain.chat_models.base import BaseChatModel
from langchain.schema import BaseMessage, AIMessage
from pydantic import PrivateAttr

class HuggingFaceChat(BaseChatModel):
    _api_url: str = PrivateAttr()
    _headers: dict = PrivateAttr()

    def __init__(self, 
                 api_key: str = "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", 
                 model_id: str = "meta-llama/Llama-3.1-8B-Instruct", 
                 **kwargs):
        super().__init__(**kwargs)

        if not api_key:
            raise ValueError("❌ Hugging Face API key not provided.")
        
        self._api_url = f"https://api-inference.huggingface.co/models/{model_id}"
        self._headers = {
            "Authorization": f"Bearer {api_key}"
        }

    def _convert_message(self, message: BaseMessage) -> str:
        return message.content if hasattr(message, "content") else str(message)

    def _generate(self, messages: List[BaseMessage], stop=None) -> AIMessage:
        full_prompt = "\n".join(self._convert_message(m) for m in messages)
        payload = {
            "inputs": full_prompt,
            "parameters": {"max_new_tokens": 512, "temperature": 0.7},
        }

        response = requests.post(self._api_url, headers=self._headers, json=payload)

        if response.status_code != 200:
            raise RuntimeError(f"❌ Hugging Face API request failed: {response.status_code} - {response.text}")

        data = response.json()
        print(response)
        if isinstance(data, dict) and data.get("error"):
            raise ValueError(f"❌ Hugging Face API error: {data['error']}")

        if isinstance(data, list) and "generated_text" in data[0]:
            generated_text = data[0]["generated_text"]
        else:
            generated_text = data[0] if isinstance(data, list) else str(data)

        return generated_text.replace('\n', '').split("[/INST]")[-1].strip()

    def _call(self, messages: List[BaseMessage], **kwargs) -> AIMessage:
        return self._generate(messages)

    @property
    def _llm_type(self) -> str:
        return "huggingface-chat"


# import os
# from openai import OpenAI
# from typing import List
# from langchain.chat_models.base import BaseChatModel
# from langchain.schema import BaseMessage, AIMessage
# from pydantic import PrivateAttr

# class OpenRouterChat(BaseChatModel):
#     _client: OpenAI = PrivateAttr()

#     def __init__(self, api_key=
#                  "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", base_url=None, **kwargs):
#         super().__init__(**kwargs)
#         api_key = api_key #or os.getenv("OPENROUTER_API_KEY")
#         base_url = base_url or "https://openrouter.ai/api/v1"

#         if not api_key:
#             raise ValueError("❌ OpenRouter API key not provided or found in env.")

#         self._client = OpenAI(api_key=api_key, base_url=base_url)

#     def _convert_message(self, message: BaseMessage) -> dict:
#         role = getattr(message, "type", "user")
#         if role not in ["user", "assistant", "system"]:
#             role = "user"  # fallback default
#         return {"role": role, "content": message}

#     def _generate(self, messages: BaseMessage, stop=None) -> AIMessage:
#         formatted_messages = [self._convert_message(messages)]#[self._convert_message(msg) for msg in messages]
#         print("DEBUG: Formatted Messages:", formatted_messages)
#         try:
#             completion = self._client.chat.completions.create(
#                 model="openai/gpt-4-turbo",
#                 messages=formatted_messages,
#                 extra_headers={
#                     "HTTP-Referer": "https://your-site.com",
#                     "X-Title": "RAG Agent Assistant",
#                 },
#                 extra_body={}
#             )
#         except Exception as e:
#             raise RuntimeError(f"❌ Request to OpenRouter failed: {e}")
#         print(completion)
#         if not completion or not completion.choices:
#             raise ValueError("❌ No choices returned from OpenRouter")

#         # You can inspect the full response if needed
#         # print("DEBUG: Full Completion Response:", completion)
#         print(completion)
#         return completion.choices[0].message.content

#     def _call(self, messages: List[BaseMessage], **kwargs) -> AIMessage:
#         return self._generate(messages)

#     @property
#     def _llm_type(self) -> str:
#         return "openrouter-chat"
