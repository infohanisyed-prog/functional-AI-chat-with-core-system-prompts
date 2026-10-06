import os
from typing import List, Dict

from groq import Groq

from .prompts import SYSTEM_PROMPT


class GroqChatService:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is not configured.")

        self.client = Groq(api_key=api_key)
        self.model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    def generate(self, history: List[Dict[str, str]]) -> str:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}, *history]

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2,
            max_tokens=700,
        )

        return completion.choices[0].message.content or ""
