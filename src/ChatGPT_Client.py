from openai import OpenAI
from pathlib import Path
import json

class ApiClientCreator():
    
    def __init__(self, file_name="config.json", timeout=60):
        self.client = None
        self.__setup_client(timeout, file_name)

    
    def get_client(self):
        return self.client
    
    
    def __setup_client(self, timeout, file_name):
        #trys to open the json config file to read the api key
        #programm is exited if its fails 
        try:
            file_path = Path(__file__).parent / file_name
            with file_path.open(mode="r", encoding="utf-8") as file:
                data = json.load(file)
            api_key = data["api_key"]
        except OSError as e:
            print(f"Could not read Api key from file: {file_path}")
            print(f"Exeption: {e}")
            exit()

        #configure client 
        options = {
            'api_key': api_key,
            'timeout': timeout
        }

        #create client
        self.client = OpenAI(**options)
        #print("Client Setup: Done")
