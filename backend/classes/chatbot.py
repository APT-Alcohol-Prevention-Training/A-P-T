import os
from flask import session
from openai import OpenAI
class Chatbot:
    default_model = os.getenv('OPENAI_DEFAULT_MODEL')

    # Function to get chatbot response
    @classmethod
    def get_response(cls, chatbot_type, user_message, api_key):
        # Use session-specific model or default
        api_key = os.getenv('OPENAI_API_KEY')  # 환경 변수 직접 사용
        fine_tuned_model = os.getenv('OPENAI_DEFAULT_MODEL')  # 환경 변수 직접 사용
        
        # fine_tuned_model = session.get('fine_tuned_model', cls.default_model)

        if not api_key or not fine_tuned_model:
            return "Please configure API key and model ID first."

        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)

        if chatbot_type == 'A':
            style_instruction = "Respond in an informal, friendly, and casual manner."
        else:
            style_instruction = "Respond in a formal and official manner."

        messages = [
            {"role": "system", "content": f"{style_instruction}"},
            {"role": "user", "content": user_message}
        ]

        try:
            response = client.chat.completions.create(
                model=fine_tuned_model,  # Use the fine-tuned model from session or class default
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error in OpenAI API call: {e}")
            return "I'm sorry, I encountered an error. Please try again later."
        