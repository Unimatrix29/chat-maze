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
        """
        Initializes the chatgpt_movment class with the given API client and model.

        Args:
            chatgpt (object): The API client used for accessing ChatGPT services.
            model (str): The name of the ChatGPT model.
        """
        self.chatgpt = chatgpt
        self.model = model
        self.move_options = {"up": [0, -1], "down": [0, 1], "left": [-1, 0], "right": [1, 0], "weird": [0, 0], "deny": [-1, -1]}
        
    def get_vector(self, userInput, temperature, sysPrompt):
        """
        Generates a movement vector based on user input.

        Args:
            userInput (str): The user's input.
            temperature (float): The temperature parameter for generating responses.
            sysPrompt (str): The system prompt to be used for generating responses.

        Returns:
            tuple: A tuple containing the movement vector and the generated response text.
        """
        
        # The API requires a specific format for the message
        # For reference, see the ChatGPT_Controller.py file
        message = self.chatgpt.construct_message(userInput, sysPrompt)                
        
        try:
            chat_response = self.chatgpt.text_to_text(message, temperature, self.model)
        except openai.APIError as e: 
            raise e 
        
        # Extract the content of the response
        # For reference, see the OpenAI API documentation: https://platform.openai.com/docs/guides/chat-completions/response-format
        content = chat_response.choices[0].message.content
        
        self.chatgpt.set_history("assistant", content)
        
        print("ChatGPT: " + content)
        
        # Parse the response
        # For reference, see the prompt documentation
        text = content.split("|")
    
        direction = text[0].lower().strip()
        if direction in self.move_options:
            move_vector = self.move_options[direction]
        else:
            move_vector = self.move_options["deny"]
            
        return move_vector, text[1]