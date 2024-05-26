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
        
        with open(self.file_tts_out, "wb") as audio_file:
            for chunk in response.iter_bytes(chunk_size=1024):
                if chunk:
                    audio_file.write(chunk)
    
    
    def audio_to_text(self, user_audio, prompt=""):
        
        model = "whisper-1"
        
        if not self.file_stt_in.exists():
            raise FileNotFoundError
            
        try:
            with open(self.file_stt_in, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model=model,
                    file=audio_file,
                    prompt=prompt,
                    language="de"

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
    
    
    @staticmethod
    def TTS_test():
        from ChatGPT_Client import ApiClientCreator
        import pygame
        
        AC = ApiClientCreator()
        client = AC.get_client()

        speech_file = Path(__file__).parent / "speech.mp3"
        speech_file = speech_file.resolve()
        
        TTS = ChatGPT(client, speech_file)

        pygame.mixer.init()

        texts = ["Das ist der erste Test", "Hier kommt gleich noch einer.", "Alle guten Dinge sind drei.", "Und weils so schön war hier noch ein vierter."]


        for text in texts:
            TTS.text_to_audio(text)

            pygame.mixer.music.load(speech_file)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            pygame.mixer.music.unload()           