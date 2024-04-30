import random 
from openai import OpenAI

GPT_MODEL = "gpt-3.5-turbo"
API_KEY = "sk-proj-6zZsLWAh1nhmbsAZvQdoT3BlbkFJ02kbMmKx5qPw8sbUZvCA"
SYSTEM_PROMPT = "You ar a helpful mathe teacher."

class Controller():

    def __init__(self):
        self.userPrompt = ""

        self.client = OpenAI(api_key=API_KEY)
        self.client.api_key
        self.move_options = {"up": [0, -1], "down": [0, 1], "left": [-1, 0], "right": [1, 0], "deny": [0, 0]}

    def __gpt_call(self):
        
        massage = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": self.userPrompt}
        ]

        response = self.client.chat.completions.create(
        model=GPT_MODEL,
        messages=[
                {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
                {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
            ]
        )

        print(response.choices[0].message)