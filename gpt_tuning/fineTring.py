
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
if not client.api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

# Upload the training file
try:
    with open("training_data.jsonl", "rb") as file:
        response = client.files.create(file=file, purpose="fine-tune")
        training_file_id = response.id
        # Training file uploaded successfully. File ID: {training_file_id}
except FileNotFoundError:
    # The file 'training_data.jsonl' was not found.
    exit(1)
except Exception as e:
    # An error occurred while uploading the file: {e}
    exit(1)

# Fine-tune the model and return the fine-tuning job ID
model_name = "gpt-4o-mini-2024-07-18"  # Updated to a model that supports fine-tuning
try:
    fine_tune_response = client.fine_tuning.jobs.create(
        training_file=training_file_id, 
        model=model_name
    )
    fine_tune_job_id = fine_tune_response.id
    # Fine-tuning job initiated successfully. Job ID: {fine_tune_job_id}
    
    # Return the fine-tuning job ID for future use
    # Use this Fine-tuning Job ID: {fine_tune_job_id}
    
except Exception as e:
    # An error occurred while initiating fine-tuning: {e}
    exit(1)
