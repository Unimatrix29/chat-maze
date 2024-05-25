import openai

class chatgpt_base():

    def __init__(self, client, system_prompt="", gpt_model="gpt-3.5-turbo"):
        self.client = client
        self.gpt_model = gpt_model
        self.system_prompt = {"content": system_prompt, "role": "system"}


    def chat_completion_request(self, userInput, history, temperature):

        message = self.__construct_message(userInput, history)

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
        

    def __construct_message(self, userInput, history):
        #format user prompt for api 
        userPrompt = {"content": userInput, "role": "user"}

        #construct message for api call 
        message = []
        message.append(self.system_prompt)
        if history is not None:
            message.append(history)
        message.append(userPrompt)
        
        return message  