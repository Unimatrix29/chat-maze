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
        
        if not self.file_user_input.exists():
            self.file_user_input.touch()
        
        self.file_user_input = Path(__file__).parent / "user_input.wav"
        self.file_user_input.resolve()
                    
        if not self.file_tts_out.exists():
            self.file_tts_out.touch()


    def text_to_text(self, message, temperature=1):
        #try api call, return response object 
        try:
            textResponse = self.client.chat.completions.create(
                model=self.gpt_model,
                messages=message,
                temperature=temperature
            ) 
            
            return textResponse
        except openai.APIError as e:
            print(e)
            raise e
        
    
    def text_to_audio(self, text, voice="onyx", model="tts-1"):
        try:
            audioResponse = self.client.audio.speech.create(
                model=model,
                voice=voice,
                input=text,
                response_format="mp3",
            )
            
            self.write_audio_to_file(audioResponse)
               
        except openai.APIError as e:
            print("Api call failed!")
            print(e)
            raise e 
        
    
    def audio_to_text(self, prompt="", model ="whisper-1"):
        try:
            with open(self.file_user_input, "rb") as audio_file:
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
        
    
    def write_audio_to_file(self, audio_data):
        try:
            with open(self.file_tts_out, "wb") as audio_file:
                for chunk in audio_data.iter_bytes(chunk_size=1024):
                    if chunk:
                        audio_file.write(chunk)
        except Exception as e: 
            print(f"Failed to write to audio file!")
            print(e)
        
    @staticmethod
    def construct_message(userInput, system_prompt, history=None):
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