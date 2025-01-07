# Logger test
import os
from logger import Logger

def test_logger():
    # Initialize the logger (creates the logs directory if it doesn't exist)
    Logger.init()
    
    # Define test data
    chatbot_type = "A"
    user_message = "Hello, how are you?"
    bot_response = "I'm a bot, but I'm doing well. How can I assist you?"
    user_ip = "192.168.1.10"
    
    # Log a conversation
    Logger.log_conversation(chatbot_type, user_message, bot_response, user_ip)
    
    # Check if the log file was created
    if os.path.exists(Logger.log_file_path):
        print(f"Log file found at: {Logger.log_file_path}")
        
        # Read and print the contents of the log file
        with open(Logger.log_file_path, 'r', encoding='utf-8') as log_file:
            logs = log_file.read()
            print("Log file contents:")
            print(logs)
    else:
        print("Log file was not created.")

if __name__ == "__main__":
    test_logger()


# Authmanager test
