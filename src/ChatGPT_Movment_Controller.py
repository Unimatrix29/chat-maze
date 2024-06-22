import openai
from openai import OpenAI
from ChatGPT_Controller import ChatGPT

class chatgpt_movment():
    
    def __init__(self, chatgpt, model):
        self.chatgpt = chatgpt
        self.model = model
        self.move_options = {"up": [0, -1], "down": [0, 1], "left": [-1, 0], "right": [1, 0], "weird": [0, 0], "deny": [-1, -1]}
        
        
    def get_vector(self, userInput, temperature, sysPrompt):
        
        message = self.chatgpt.construct_message(userInput, sysPrompt)                
        
        #api response 
        try:
            chat_response = self.chatgpt.text_to_text(message, temperature, self.model)
        except openai.APIError as e: 
            raise e 
        
        content = chat_response.choices[0].message.content
        self.chatgpt.set_history( "assistant", content)
        
        print("ChatGPT: " + content)
        
        text = content.split("|")
    
        #convert to vector
        direction = text[0].lower().strip()
        if direction in self.move_options:
            move_vector = self.move_options[direction]
        else:
            move_vector = self.move_options["deny"]
            
        return move_vector, text[1]