import openai
from openai import OpenAI
from ChatGPT_Controller import chatgpt_base

class chatgpt_movment():
    
    def __init__(self, client, system_prompt="", history=None, gpt_model="gpt-3.5-turbo"):
        self.history = history
        self.textChatGPT = chatgpt_base(client, system_prompt, gpt_model)
        self.move_options = {"up": [0, -1], "down": [0, 1], "left": [-1, 0], "right": [1, 0], "deny": [0, 0]}
        
        
    def get_movement_vector(self, userInput, temperature=None):
        #api response 
        try:
            chat_response = self.textChatGPT.chat_completion_request(userInput, history=self.history, temperature=temperature)
        except Exception as e: 
            return e 
        
        #get api response content
        content = chat_response.choices[0].message.content.lower().strip()
        print("ChatGPT: " + content)
        
        #convert to vector
        if content in self.move_options:
            move_vector = self.move_options[content]
        else:
            move_vector = self.move_options["deny"]
            
        return move_vector
        