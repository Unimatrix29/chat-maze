import openai
from openai import OpenAI
from ChatGPT_Controller import ChatGPT

class chatgpt_movment():
    """
    Represents a ChatGPT Movement Controller.

    This class is responsible for controlling the movement via a ChatGPT model based on user input.

    Attributes:
        chatgpt (object): The API client used for accessing ChatGPT services.
        model (str): The name of the ChatGPT model.
        move_options (dict): A dictionary mapping movement directions to their corresponding move vectors.

    Methods:
        get_vector(userInput, temperature, sysPrompt): Generates a movement vector based on user input.

    """

    def __init__(self, chatgpt, model):
        self.chatgpt = chatgpt
        self.model = model
        self.move_options = {"up": [0, -1], "down": [0, 1], "left": [-1, 0], "right": [1, 0], "weird": [0, 0], "deny": [-1, -1]}
        
        
    def get_vector(self, userInput, temperature, sysPrompt):
        """
        Generates a movement vector based on user input.

        :param userInput: The user's input.
        :type userInput: str
        :param temperature: The temperature parameter for generating responses.
        :type temperature: float
        :param sysPrompt: The system prompt to be used for generating responses.
        :type sysPrompt: str
        :returns: A tuple containing the movement vector and the generated response text.
        :rtype: tuple
        """
        
        #the API reqiures a specific format for the message
        #for reference, see the ChatGPT_Controller.py file
        message = self.chatgpt.construct_message(userInput, sysPrompt)                
        
        try:
            chat_response = self.chatgpt.text_to_text(message, temperature, self.model)
        except openai.APIError as e: 
            raise e 
        
        #extract the content of the response
        #for reference, see the OPenAI API documentation: https://platform.openai.com/docs/api-reference/making-requests
        content = chat_response.choices[0].message.content
        
        self.chatgpt.set_history( "assistant", content)
        
        print("ChatGPT: " + content)
        
        #parse the response
        #for reference, see the prompt documentation
        text = content.split("|")
    
        direction = text[0].lower().strip()
        if direction in self.move_options:
            move_vector = self.move_options[direction]
        else:
            move_vector = self.move_options["deny"]
            
        return move_vector, text[1]