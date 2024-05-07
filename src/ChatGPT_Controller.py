from openai import OpenAI
import json
import os 

class ChatGPT():

    def __init__(self, system_prompt, config_file, history=None, gpt_model="gpt-3.5-turbo", timeout=None):
        self.gpt_model = gpt_model
        self.system_prompt = {"content": system_prompt, "role": "user"}
        self.history = history
        self.move_options = {"up": [0, -1], "down": [0, 1], "left": [-1, 0], "right": [1, 0], "deny": [0, 0]}
        self.__setup_client(timeout=timeout, file=config_file)


    def get_movement_vector(self, userInput, temperature=None):

        #create message
        message = self.__construct_message(userInput=userInput, history=self.history)
        
        #api response 
        chat_response = self.__chat_completion_request(message=message, temperature=temperature)
        #test
        print(f"\n{chat_response}\n")

        #get api response content
        content = chat_response.choices[0].message.content.lower().strip()
        #test
        print(chat_response.choices[0].message)

        #convert to vector
        if content in self.move_options:
            move_vector = self.move_options[content]
        else:
            move_vector = self.move_options["deny"]
        
        return move_vector


    def __chat_completion_request(self, message, temperature):

        #try api call, return response object 
        try:
            response = self.client.chat.completions.create(
                model=self.gpt_model,
                messages=message,
                temperature=temperature
            )
            return response
        except Exception as e: 
            print("An error occurred!")
            print(f"Exeption: {e}")
            pass
        

    def __construct_message(self, userInput, history):
        #format user prompt for api 
        userPrompt = {"content": userInput, "role": "user"}

        #construct message for api call 
        message = []
        message.append(self.system_prompt)
        if history is not None:
            message.append(history)
        message.append(userPrompt)

        #Test
        print("Message:")
        for dic in message:
            print(dic)
        print("Message Setup: Done")

        return message  


    def __setup_client(self, timeout, file):
        #trys to open the json config file to read the api key
        #programm is exited if its fails 
        try:
            here = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(here, file)
            with open(file_path, "r") as file:
                data = json.load(file)
            api_key = data["key"]
        except Exception as e:
            print(f"Could not read api key from file: {file_path}")
            print(f"Exeption: {e}")
            exit()

        #configure client 
        options = {
            'api_key': api_key,
            'timeout': timeout
        }

        #create client
        self.client = OpenAI(**options)
        print("Client Setup: Done")

#TEST
# chatGPT = ChatGPT(system_prompt="Repet everything I say.", config_file="config.json", timeout=30)
# mVector = chatGPT.get_movement_vector(userInput="up")
# print(mVector)