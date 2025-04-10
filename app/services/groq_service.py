from app.models.conversation import Conversation
from app.core.config import GROQ_API_KEY
from groq import Groq
from app.schemas.chat import UserInput

# System prompt to guide the bot's responses
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "Hey! I'm your friendly assistant for maps, directions, and location help. 🗺️\n\n"
        "I always keep my answers short (2 sentences max).\n"
        "If someone asks about anything else like coding, math, or unrelated stuff, just reply:\n"
        "'Sorry, I can only help with map and navigation-related questions.'"
    )
}



class GroqService:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

    def get_response(self, user_input: UserInput) -> str:
        conversation = Conversation()

        # Add system prompt to the conversation
        conversation.add_message(SYSTEM_PROMPT["role"], SYSTEM_PROMPT["content"])

        # Assign role as "user" for the user message
        role = "user"

        # Add user message to the conversation
        conversation.add_message(role, user_input.message)

        try:
            # Send conversation to the Groq API and get the response
            completion = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=conversation.get_messages(),
                temperature=1,
                max_tokens=1024,
                top_p=1,
                stream=True,
                stop=None,
            )

            # Collect the response from the streamed chunks
            response = ""
            for chunk in completion:
                response += chunk.choices[0].delta.content or ""

            return response

        except Exception as e:
            raise Exception(f"Error with Groq API: {str(e)}")
