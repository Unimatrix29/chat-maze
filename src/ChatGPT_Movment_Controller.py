import openai
from openai import OpenAI
from ChatGPT_Controller import ChatGPT

class chatgpt_movment():
    
    def __init__(self, chatgpt, system_prompt):
        self.chatgpt = chatgpt
        self.sysPrompt = system_prompt
        self.move_options = {"up": [0, -1], "down": [0, 1], "left": [-1, 0], "right": [1, 0], "deny": [0, 0]}
        
        
    def get_vector(self, userInput, temperature):
        
        message = ChatGPT.construct_message(userInput, self.sysPrompt)
        
        #api response 
        try:
            chat_response = self.chatgpt.text_to_text(message, temperature)
        except Exception as e: 
            return e 
        
        #get api response content
        content = chat_response.lower().strip()
        print("ChatGPT: " + content)
        

        #convert to vector
        if content in self.move_options:
            move_vector = self.move_options[content]
        else:
            move_vector = self.move_options["deny"]
            
        return move_vector, content
        