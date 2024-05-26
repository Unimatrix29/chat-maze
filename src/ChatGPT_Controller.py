import openai
from pathlib import Path

class ChatGPT():

    def __init__(self, client, gpt_model="gpt-3.5-turbo"):
        self.client = client
        self.gpt_model = gpt_model


    def chat_completion_request(self, message, temperature):
        #try api call, return response object 
        try:
            response = self.client.chat.completions.create(
                model=self.gpt_model,
                messages=message,
                temperature=temperature
            ) 
            
            return response
        except openai.APITimeoutError as e:
            print(f"OpenAI API timeout.")
            print(e)
            raise e
        except openai._exceptions as e:
            print(e)
            raise e
        
    @staticmethod
    def construct_message(userInput, history=None, system_prompt="",):
        #format user and system prompt for api 
        userPrompt = {"content": userInput, "role": "user"}
        system_prompt = {"content": system_prompt, "role": "system"}

        #construct message for api call 
        message = []
        message.append(system_prompt)
        if history is not None:
            message.append(history)
        message.append(userPrompt)
        
        return message  