# pipeline/mistral_utils.py

from mistralai import Mistral, UserMessage
from dotenv import load_dotenv
import time
import os

load_dotenv()
api_key = os.environ["MISTRAL_API_KEY"]
client = Mistral(api_key=api_key)
model = "mistral-medium"

def query_mistral(prompt: str) -> str:
    time.sleep(3)
    messages = [
        UserMessage(role="user", content=prompt)
    ]

    chat_response = client.chat.complete(
        model=model,
        messages=messages,
    )

    return chat_response.choices[0].message.content.strip()
