from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import ollama

# from openai import OpenAI

# load_dotenv()

app = FastAPI()

# # OpenAI client
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Request schema
class FeedbackRequest(BaseModel):
    subject: str
    notes: str


# API endpoint
@app.post("/get_feedback")
def get_feedback(data: FeedbackRequest):

    prompt = f"""
    A teacher conducted a class.

    Subject: {data.subject}

    Class Notes:
    {data.notes}

    Provide constructive feedback for the teacher.
    Give:
    - strengths
    - areas to improve
    - suggestions
    """

    response = ollama.chat(
        model="llama3.2.1b",
        messages=[
            {"role": "user", "content": prompt}
        ],
        options={
        "num_predict": 150
    }
    )

    feedback = response["message"]["content"]

    return {
        "subject": data.subject,
        "feedback": feedback
    }

