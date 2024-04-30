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
        

    def gpt_call(self):
        
        #construct massage for api call 
        massage = [SYSTEM_PROMPT]
        massage.extend(self.userHistory)
        massage.append(self.userPrompt)

        #test
        for dic in massage:

            print(dic)

        #api call 
        response = self.client.chat.completions.create(
        model=GPT_MODEL,
        messages=massage
        )

        #get response massage
        response_massage = response.choices[0].message

        #safe user history
        self.userHistory.append(response_massage)
        #not in here
        self.userHistory.append(self.userPrompt)

        #test
        print(response_massage.content)

        
        return response_massage.content


 
#test
c = Controller()

c.gpt_call()