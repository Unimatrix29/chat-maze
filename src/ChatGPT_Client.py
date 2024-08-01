from openai import OpenAI
from pathlib import Path
import json

class ApiClientCreator():
    """
    This class provides a static method to create an API client for ChatGPT.
    The client is created by reading the API key from a JSON config file.
    """

    @staticmethod
    def get_client(file_name="config.json", timeout=60):
        """
        Creates and returns an API client for ChatGPT.

        :param file_name: The name of the JSON config file (default: "config.json").
        :param timeout: The timeout value for API requests in seconds (default: 60).
        :return: An instance of the API client.
        """
        
        # Try to open the JSON config file to read the API key.
        # Exit the program if it fails.
        try:
            file_path = Path(__file__).parent / file_name
            with file_path.open(mode="r", encoding="utf-8") as file:
                data = json.load(file)
            api_key = data["api_key"]
        except OSError as e:
            print(f"Could not read API key from file: {file_path}")
            print(f"Exception: {e}")
            exit()

        # Configure the client.
        options = {
            'api_key': api_key,
            'timeout': timeout
        }

        # Create the client.
        client = OpenAI(**options)
        return client