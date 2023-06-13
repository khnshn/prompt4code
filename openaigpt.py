import os
import openai
from dotenv import load_dotenv

load_dotenv()

api_key = str(os.getenv("API_KEY"))

openai.api_key = api_key


def chat(messages, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )
    return response["choices"][0]["message"]["content"]


if __name__ == "__main__":
    print("import this module")
