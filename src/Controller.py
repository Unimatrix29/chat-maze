from openai import OpenAI

GPT_MODEL = "gpt-3.5-turbo"

####################################################################
#THIS KEY IS NOT WORKING, NEED TO ASK RODNER FOR AN ACTUAL KEY 
API_KEY = "sk-proj-6zZsLWAh1nhmbsAZvQdoT3BlbkFJ02kbMmKx5qPw8sbUZvCA"
#####################################################################

SYSTEM_PROMPT =  {"content": "You ar a helpful mathe teacher.", "role": "system"}

class Controller():

    def __init__(self):
        self.userHistory = []

        self.move_options = {"up": [0, -1], "down": [0, 1], "left": [-1, 0], "right": [1, 0], "deny": [0, 0]}

        self.client = OpenAI(api_key=API_KEY)

    def get_movement_vector(self, userInput="deny"):
        userPrompt = {"content": userInput, "role": "user"}
        message = self.__construct_message(prompt=userPrompt)
        
        chat_response = self.__chat_completion_request(message=message)

        self.userHistory.extend(userPrompt, chat_response.choices[0].message)
        move_vector = self.move_options[chat_response.choices[0].message.content.lower().strip()]

        return move_vector

    def __chat_completion_request(self, message, seed=None, model=GPT_MODEL):
        #try api call, return response object 
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=message,
                seed=seed
            )
            return response
        except Exception as e: 
            print("Something has gone wrong!")
            print(f"Exeption: {e}")
            return None
        
    def __construct_message(self, prompt, history):
        #construct message for api call 
        message = [SYSTEM_PROMPT]
        message.extend(history,  prompt)
        return message  