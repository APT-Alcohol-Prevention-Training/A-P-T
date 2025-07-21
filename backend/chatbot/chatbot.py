from openai import OpenAI
from config import current_config


class Chatbot:
    @classmethod
    def get_response(cls, chatbot_type, user_message, risk_score=None, api_key=None, conversation_context=None):
        """
        Process the user message using the specified chatbot type and return the response.
        """
        
        # Check if this is a response to the party scenario
        if conversation_context and "party_scenario" in conversation_context:
            scenario_num = conversation_context.get("party_scenario", 1)
            if scenario_num == 1:
                return cls._handle_party_scenario_response(user_message)
            elif scenario_num == 2:
                return cls._handle_concert_scenario_response(user_message)
            elif scenario_num == 3:
                return cls._handle_date_scenario_response(user_message)
    

        # Get configuration
        config = current_config()
        openai_config = config.get_openai_config()
        
        # Use provided API key or get from config
        if not api_key:
            api_key = openai_config['api_key']
        
        if not api_key:
            raise ValueError("Missing OpenAI API key")

        # Initialize the OpenAI client
        client = OpenAI(
            api_key=api_key,
            timeout=openai_config['timeout'],
            max_retries=openai_config['max_retries']
        )

        # Map chatbot types to style instructions.
        style_instructions = {
            "ai": "Respond in an informal, friendly, and casual manner.",
            "student": "Respond in an inquisitive, energetic, and slightly informal manner.",
            "doctor": "Respond in a formal, professional, and knowledgeable manner.",
        }
        style_instruction = style_instructions.get(chatbot_type)
        if not style_instruction:
            raise ValueError("Invalid chatbot type.")

        messages = [
            {"role": "system", "content": style_instruction},
            {"role": "user", "content": user_message},
        ]

        try:
            response = client.chat.completions.create(
                model=openai_config['model'],
                messages=messages,
                temperature=openai_config['temperature'],
                max_tokens=openai_config['max_tokens'],
                top_p=openai_config['top_p'],
                frequency_penalty=openai_config['frequency_penalty'],
                presence_penalty=openai_config['presence_penalty']
            )
            content = response.choices[0].message.content
            if content is None:
                raise RuntimeError("No content was returned from the API.")
            return content.strip()
        except Exception as e:
            config = current_config()
            if config.DEBUG:
                raise RuntimeError(f"OpenAI API error: {str(e)}")
            else:
                raise RuntimeError("I'm sorry, I encountered an error. Please try again later.")
    
    @classmethod
    def _handle_party_scenario_response(cls, user_message):
        """
        Handle responses to the party scenario question
        """
        # Define appropriate responses and their feedback
        appropriate_responses = {
            "not drinking": {
                "keywords": ["not drinking", "don't drink", "i'm good", "no thanks", "i don't drink"],
                "feedback": "Nice. That's clear, confident, and respectful. Most people won't push further after that kind of response."
            },
            "driving": {
                "keywords": ["drive", "driving", "driver", "car", "dd", "designated driver"],
                "feedback": "Smart move—safety is always a good reason. Giving a specific, practical excuse helps take the pressure off."
            },
            "maybe later": {
                "keywords": ["maybe later", "later", "not now", "not right now"],
                "feedback": "That's okay too—sometimes deflecting helps avoid confrontation. But sometimes it might invite more pressure later."
            },
            "alternative": {
                "keywords": ["soda", "water", "juice", "something else", "non-alcoholic", "soft drink"],
                "feedback": "Offering an alternative is a smooth strategy. People usually move on if you're holding a drink—even if it's not alcohol."
            }
        }
        
        # Check if response matches any appropriate category
        user_message_lower = user_message.lower()
        
        for _, data in appropriate_responses.items():
            if any(keyword in user_message_lower for keyword in data["keywords"]):
                return data["feedback"]
        
        # If no appropriate response was found, provide a hint
        hint_response = "That's one way to respond, but let me give you a hint for a better answer. Try being more direct and confident. You could say something like 'No thanks, I'm not drinking tonight' or give a specific reason like 'I'm driving later.' Having a clear, firm response ready helps you handle peer pressure more effectively."
        
        return hint_response
    
    @classmethod
    def _handle_concert_scenario_response(cls, user_message):
        """
        Handle responses to the concert pre-game scenario question
        """
        # Define appropriate responses and their feedback
        appropriate_responses = {
            "pass_tonight": {
                "keywords": ["pass tonight", "want to remember", "remember the concert", "not tonight"],
                "feedback": "That's a powerful reason. Framing your choice positively shows you value the experience."
            },
            "meet_there": {
                "keywords": ["meet you there", "i'll meet", "see you there", "skip pre-gaming", "skipping"],
                "feedback": "That's a solid boundary—joining later helps avoid early pressure."
            },
            "food_instead": {
                "keywords": ["get food", "food before", "eat instead", "grab food", "dinner"],
                "feedback": "Offering an alternative is a great strategy. Redirecting plans can shift the tone without causing conflict."
            },
            "might_come": {
                "keywords": ["might come", "come by", "but not drink", "won't drink"],
                "feedback": "This keeps your options open, but some people might keep pushing."
            }
        }
        
        # Check if response matches any appropriate category
        user_message_lower = user_message.lower()
        
        for _, data in appropriate_responses.items():
            if any(keyword in user_message_lower for keyword in data["keywords"]):
                return data["feedback"]
        
        # If no appropriate response was found, provide a hint
        hint_response = "That's one approach, but here's a hint for a better answer: Try suggesting an alternative activity or being clear about your boundaries. You could say 'I'll pass on pre-gaming but meet you at the concert' or 'Let's grab food before instead.' This shows you want to hang out but on your terms."
        
        return hint_response
    
    @classmethod
    def _handle_date_scenario_response(cls, user_message):
        """
        Handle responses to the first date scenario question
        """
        # Define appropriate responses and their feedback
        appropriate_responses = {
            "not_drinking": {
                "keywords": ["not drinking tonight", "don't drink", "still having a great time", "having fun", "great time"],
                "feedback": "That's perfect—you're holding your boundary while keeping things positive."
            },
            "water": {
                "keywords": ["water", "just water", "have water", "water for now"],
                "feedback": "Simple and smooth. Sometimes people don't even notice."
            },
            "cheers": {
                "keywords": ["don't really drink", "cheers to you", "don't drink much", "cheers"],
                "feedback": "Acknowledging them while making your choice clear is a great move."
            },
            "dessert": {
                "keywords": ["dessert", "split a dessert", "want to split", "food", "something else"],
                "feedback": "Redirection with charm! Offering something else keeps the vibe friendly and light."
            }
        }
        
        # Check if response matches any appropriate category
        user_message_lower = user_message.lower()
        
        for _, data in appropriate_responses.items():
            if any(keyword in user_message_lower for keyword in data["keywords"]):
                return data["feedback"]
        
        # If no appropriate response was found, provide a hint
        hint_response = "That's one way to handle it, but here's a hint for a better answer: Try being clear about your choice while keeping the mood positive. You could say 'I'm not drinking tonight, but I'm having a great time' or suggest an alternative like 'Want to split a dessert instead?' This shows you're engaged in the date while maintaining your boundaries."
        
        return hint_response
