import random 
from openai import OpenAI

GPT_MODEL = "gpt-3.5-turbo"
API_KEY = "sk-proj-6zZsLWAh1nhmbsAZvQdoT3BlbkFJ02kbMmKx5qPw8sbUZvCA"
SYSTEM_PROMPT =  {"content": "You ar a helpful mathe teacher.", "role": "system"}

class Controller():

    def __init__(self):
        self.userPrompt = {"content": "", "role": "user"}
        self.userHistory = []
        self.move_options = {"up": [0, -1], "down": [0, 1], "left": [-1, 0], "right": [1, 0], "deny": [0, 0]}

        self.client = OpenAI(api_key=API_KEY)
        self.client.api_key
        

    def __gpt_call(self):
        
        massage = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": self.userPrompt}
        ]

        response = self.client.chat.completions.create(
        model=GPT_MODEL,
        messages=massage
        )
        
        response_content = response.choices[0].message.content

        print(response_content)

        return response_content