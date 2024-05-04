from openai import OpenAI
import json
import os 

class ChatGPT():

    def __init__(self, system_prompt, config_file, history=None, gpt_model="gpt-3.5-turbo", timeout=None):
        self.gpt_model = gpt_model
        self.system_prompt = {"content": system_prompt, "role": "user"}
        self.history = history
        self.move_options = {"up": [0, -1], "down": [0, 1], "left": [-1, 0], "right": [1, 0], "deny": [0, 0]}

    def get_movement_vector(self, userInput="deny"):
        #format user prompt for api 
        userPrompt = {"content": userInput, "role": "user"}

        #make message
        message = self.__construct_message(prompt=userPrompt, history=self.userHistory)
        
        #api call 
        chat_response = self.__chat_completion_request(message=message)

        #safe user history for future calls 
        self.userHistory.extend(userPrompt, chat_response.choices[0].message)

        #get api response content
        content = chat_response.choices[0].message.content.lower().strip()

        #convert to vector
        if content in self.move_options:
            move_vector = self.move_options[content]
        else:
            move_vector = self.move_options["deny"]
        
        return move_vector

    def __chat_completion_request(self, message, seed=None, model=GPT_MODEL, api_key=API_KEY):

        #create api client
        client = OpenAI(api_key=api_key)

        #try api call, return response object 
        try:
            response = client.chat.completions.create(
                model=model,
                messages=message,
                seed=seed
            )
            return response
        except Exception as e: 
            print("Something has gone wrong!")
            print(f"Exeption: {e}")
            return None
        
    def __construct_message(self, prompt, history=None, sys_prompt=SYSTEM_PROMPT):
        #construct message for api call 
        message = []
        message.extend(sys_prompt, history,  prompt)
        return message  