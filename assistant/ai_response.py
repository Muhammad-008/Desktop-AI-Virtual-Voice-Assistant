"""AI response module using OpenAI API with fallback responses."""

import os
import re
from datetime import datetime

import openai


FALLBACK_RESPONSES = {
    "greeting": [
        "Hello! How can I help you today?",
        "Hi there! What can I do for you?",
        "Hey! I'm ready to assist you.",
    ],
    "farewell": [
        "Goodbye! Have a great day!",
        "See you later! Take care!",
        "Bye! Feel free to ask me anytime.",
    ],
    "thanks": [
        "You're welcome!",
        "Happy to help!",
        "Anytime! Let me know if you need anything else.",
    ],
    "how_are_you": [
        "I'm doing great, thanks for asking! How can I help?",
        "I'm functioning perfectly! What can I do for you?",
    ],
    "name": [
        "I'm your Desktop AI Virtual Voice Assistant!",
        "You can call me your AI Assistant. How can I help?",
    ],
    "capabilities": [
        "I can open apps, tell you the weather, control your system, "
        "answer questions, and much more! Just ask.",
    ],
    "unknown": [
        "I'm not sure I understand. Could you rephrase that?",
        "I don't have an answer for that right now. Try asking something else!",
        "Hmm, I'm not sure about that. Can I help with something else?",
    ],
}

PATTERN_MAP = [
    (r"\b(hello|hi|hey|greetings)\b", "greeting"),
    (r"\b(bye|goodbye|see you|farewell)\b", "farewell"),
    (r"\b(thanks|thank you|appreciate)\b", "thanks"),
    (r"\b(how are you|how do you do|how's it going)\b", "how_are_you"),
    (r"\b(your name|who are you|what are you)\b", "name"),
    (r"\b(what can you do|capabilities|features|help me)\b", "capabilities"),
]


class AIEngine:
    """Handles AI-powered responses using OpenAI with fallback logic."""

    def __init__(self, api_key: str = ""):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.client = None
        self.model = "gpt-3.5-turbo"
        self.conversation_history = []
        self.max_history = 20
        self._openai_available = False

        if self.api_key:
            self._init_openai()

    def _init_openai(self):
        """Initialize OpenAI client."""
        try:
            self.client = openai.OpenAI(api_key=self.api_key)
            self._openai_available = True
        except Exception:
            self._openai_available = False

    def set_api_key(self, api_key: str):
        """Update the OpenAI API key."""
        self.api_key = api_key
        if self.api_key:
            self._init_openai()
        else:
            self.client = None
            self._openai_available = False

    def is_openai_available(self) -> bool:
        """Check if OpenAI API is configured and available."""
        return self._openai_available

    def _get_fallback_response(self, text: str) -> str:
        """Get a pattern-matched fallback response."""
        import random

        text_lower = text.lower()
        for pattern, category in PATTERN_MAP:
            if re.search(pattern, text_lower):
                return random.choice(FALLBACK_RESPONSES[category])
        return random.choice(FALLBACK_RESPONSES["unknown"])

    def get_response(self, user_input: str) -> str:
        """Get AI response for user input."""
        if self._openai_available:
            return self._get_openai_response(user_input)
        return self._get_fallback_response(user_input)

    def _get_openai_response(self, user_input: str) -> str:
        """Get response from OpenAI API."""
        system_prompt = (
            "You are a helpful desktop AI voice assistant. "
            "Keep responses concise and conversational (1-3 sentences). "
            f"Current date/time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}. "
            "You can help with general questions, provide information, "
            "and assist with various tasks."
        )

        self.conversation_history.append({"role": "user", "content": user_input})

        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(self.conversation_history)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=256,
                temperature=0.7,
            )
            reply = response.choices[0].message.content.strip()
            self.conversation_history.append(
                {"role": "assistant", "content": reply}
            )
            return reply
        except Exception:
            self.conversation_history.pop()
            return self._get_fallback_response(user_input)

    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history.clear()
