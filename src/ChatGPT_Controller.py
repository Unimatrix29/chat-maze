import openai
import numpy as np 
import time
import sounddevice as sd
from pathlib import Path
from scipy.io.wavfile import write as wavWrite

class ChatGPT():

    def __init__(self, client, gpt_model="gpt-3.5-turbo", ):
        self.client = client
        self.gpt_model = gpt_model
        self.file_tts_out = Path(__file__).parent / "tts_out.mp3"
        self.file_tts_out.resolve()
        self.file_user_input = Path(__file__).parent / "user_input.wav"
        self.file_user_input.resolve()
        
        if not self.file_user_input.exists():
            self.file_user_input.touch()
            
        if not self.file_tts_out.exists():
            self.file_tts_out.touch()


    def text_to_text(self, message, temperature=1):
        #try api call, return response object 
        try:
            response = self.client.chat.completions.create(
                model=self.gpt_model,
                messages=message,
                temperature=temperature
            ) 
            
            return response
        except openai.APIError as e:
            print(e)
            raise e
        
    
    def text_to_audio(self, text, voice="onyx", model="tts-1"):
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
        
        if not user_audio.exists():
            raise FileNotFoundError
            
        try:
            with open(user_audio, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model=model,
                    file=audio_file,
                    prompt=prompt,
                    language="de",
                    response_format="json"
                )
                
            return transcript.text
        except openai.APIError as e:
            print("Api call failed!")
            print(e)
            raise e 
        except Exception as e:
            print(e)
            raise e
        
    
    def get_user_audio(self, duration=10):
        samplerate = 44100 
        
        print("Speak now...")
        data = sd.rec(int(samplerate * duration), samplerate, channels=2)
        
        while duration > 0:
            print(duration)
            duration = duration - 1
            time.sleep(1)
                    
        sd.wait()
        
        print("Recording finished!")
        
        wavWrite(self.file_user_input, samplerate, data) 
        
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
        
    
    #def get_user_audio_with_dynamic_duration(self):
        samplerate = 44100
        channel = 1
        maxDuration = 5
        inputStream = sd.InputStream(samplerate=samplerate, channels=channel)
        
        print("#" * 80)
        print("Speak now...")
        print("Press Ctrl+C to stop recording")
        print("#" * 80)
        
        inputStream.start()
        
        data = inputStream.read(samplerate * maxDuration)[0]
        print("\nRecording stoped")
        
        inputStream.stop()
        inputStream.close()   
        
        
        wavWrite(self.file_user_input, samplerate, data)
    
                            
    def TTS_test(self, text=None):
        import pygame
        
        TTS = ChatGPT(self.client)

        pygame.mixer.init()
        
        if text == None:
            text = "Das ist der erste Test. Hier kommt gleich noch einer. Alle guten Dinge sind drei. Und weils so schön war hier noch ein vierter."

        TTS.text_to_audio(text)
        pygame.mixer.music.load(self.file_tts_out)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        pygame.mixer.music.unload()    

           
#Test for speech to text and text to speech
#if __name__ == "__main__":  
#    from ChatGPT_Client import ApiClientCreator
#    import pygame
#    client = ApiClientCreator.get_client()
#    
#    chatgpt = ChatGPT(client, q)
#    
#    #chatgpt.test()
#    
#    #chatgpt.get_user_audio_with_dynamic_duration()
#    chatgpt.get_user_audio()