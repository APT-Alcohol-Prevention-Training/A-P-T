import os

from openai import OpenAI

from exceptions import AppException, ConfigurationError


class Chatbot:
    default_model = os.getenv("OPENAI_DEFAULT_MODEL")

    @classmethod
    def get_response(cls, chatbot_type, user_message, api_key):
        """
        Process the user message using the specified chatbot type and return the response.
        Utilizes the OpenAI API with the given model and API key.
        """
        # Ensure API key and model are configured via environment variables
        api_key = os.getenv("OPENAI_API_KEY")
        fine_tuned_model = os.getenv("OPENAI_DEFAULT_MODEL")

        if not api_key or not fine_tuned_model:
            raise ConfigurationError(
                "Please configure API key and model ID first.", status_code=500
            )

        # Initialize the OpenAI client
        client = OpenAI(api_key=api_key)

        # Choose style instruction based on chatbot type
        style_instruction = (
            "Respond in an informal, friendly, and casual manner."
            if chatbot_type == "A"
            else "Respond in a formal and official manner."
        )

        messages = [
            {"role": "system", "content": style_instruction},
            {"role": "user", "content": user_message},
        ]

        try:
            response = client.chat.completions.create(
                model=fine_tuned_model,
                messages=messages,
                temperature=0.7,
            )
            # Safely access the content, ensuring it's not None
            content = response.choices[0].message.content
            if content is None:
                raise AppException(
                    "No content was returned from the API.", status_code=500
                )
            return content.strip()
        except Exception:
            # Raise a generic application exception to be caught by the error handler
            raise AppException(
                "I'm sorry, I encountered an error. Please try again later.",
                status_code=500,
            )
