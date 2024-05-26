import openai
from pathlib import Path

class ChatGPT():

    def __init__(self, client, gpt_model="gpt-3.5-turbo"):
        self.client = client
        self.gpt_model = gpt_model
        self.file_tts_out = Path(__file__).parent / "tts_out.mp3"
        self.file_tts_out.resolve()
        self.file_stt_in = Path(__file__).parent / "tts_in.mp3"
        self.file_stt_in.resolve()


    def text_to_text(self, message, temperature=1):
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
        
    
    def text_to_audio(self, text, voice="onyx", model="tts-1"):
        
        if not self.file_tts_out.exists():
            self.file_tts_out.touch()
        
        try:
            response = self.client.audio.speech.create(
                model=model,
                voice=voice,
                input=text,
                response_format="mp3",
            )
        except openai.APIError as e:
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