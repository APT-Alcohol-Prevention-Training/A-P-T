import os
from openai import OpenAI
from exceptions import AppException, ConfigurationError


class Chatbot:
    @classmethod
    def get_response(cls, chatbot_type, user_message, risk_score=None, api_key=None):
        """
        Process the user message using the specified chatbot type and return the response.
        Uses risk_score (if provided) to select one of 12 API configurations.
        """

        # Build API configurations from environment variables OPENAI_API_KEY_1 ... OPENAI_API_KEY_12
        API_CONFIGS = []
        for i in range(1, 13):
            key = os.getenv(f"OPENAI_API_KEY_{i}")
            model = os.getenv(f"OPENAI_DEFAULT_MODEL_{i}")
            if not key or not model:
                raise ConfigurationError(
                    f"Missing OpenAI API config for index {i}", status_code=500
                )
            API_CONFIGS.append({"api_key": key, "model": model})

        # Determine risk level index (0: Low, 1: Moderate, 2: High, 3: Severe)
        if risk_score is not None:
            try:
                risk_score = int(risk_score)
            except ValueError:
                risk_score = 0
            if risk_score <= 3:
                risk_index = 0
            elif risk_score <= 7:
                risk_index = 1
            elif risk_score <= 12:
                risk_index = 2
            else:
                risk_index = 3
        else:
            risk_index = 0

        # Map chatbot types to an index: ai=0, student=1, doctor=2.
        chatbot_order = {"ai": 0, "student": 1, "doctor": 2}
        type_index = chatbot_order.get(chatbot_type, 0)
        # Calculate configuration index: each avatar has 4 risk levels
        config_index = type_index * 4 + risk_index

        # Select the appropriate API configuration
        config = API_CONFIGS[config_index]

        # Initialize the OpenAI client with the selected API key.
        client = OpenAI(api_key=config["api_key"])

        # Map chatbot types to style instructions.
        style_instructions = {
            "ai": "Respond in an informal, friendly, and casual manner.",
            "student": "Respond in an inquisitive, energetic, and slightly informal manner.",
            "doctor": "Respond in a formal, professional, and knowledgeable manner.",
        }
        style_instruction = style_instructions.get(chatbot_type)
        if not style_instruction:
            raise AppException("Invalid chatbot type.", status_code=400)

        messages = [
            {"role": "system", "content": style_instruction},
            {"role": "user", "content": user_message},
        ]

        try:
            response = client.chat.completions.create(
                model=config["model"],
                messages=messages,
                temperature=0.7,
            )
            content = response.choices[0].message.content
            if content is None:
                raise AppException(
                    "No content was returned from the API.", status_code=500
                )
            return content.strip()
        except Exception:
            raise AppException(
                "I'm sorry, I encountered an error. Please try again later.",
                status_code=500,
            )
