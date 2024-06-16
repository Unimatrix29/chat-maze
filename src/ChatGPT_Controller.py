import openai
import numpy as np 
import time
import sounddevice as sd
from pathlib import Path
from scipy.io.wavfile import write as wavWrite
from functools import partial

class ChatGPT():

    def __init__(self, client, max_history_length=5):
        self.client = client
        self._history = []
        self.max_length = max_history_length
        
        self.file_tts_out = Path(__file__).parent / "tts_out.wav"
        self.file_tts_out.resolve()
        
        if not self.file_tts_out.exists():
            self.file_tts_out.touch()
        
        self.file_user_input = Path(__file__).parent / "user_input.wav"
        self.file_user_input.resolve()
                     
        if not self.file_user_input.exists():
            self.file_user_input.touch()
        

    def text_to_text(self, message, temperature=1, model="gpt-3.5-turbo", _retrie=False):
        #try api call, return response object 
        try:
            textResponse = self.client.chat.completions.create(
                model=model,
                messages=message,
                temperature=temperature
            ) 
            
            #dummy Error
            #raise openai.APIError("Test Error", message, body={"error": {"message": "Dies ist ein simulierter Fehler."}})
            
            return textResponse
        except (openai.APIConnectionError or openai.InternalServerError or openai.UnprocessableEntityError) as e:
            if _retrie:
                raise e
            ttt_partial = partial(self.text_to_text, message, temperature, model)
            return ChatGPT.__error_handling(ttt_partial)
        except openai.APIError as e:
            print("Text to text Api call failed!")
            print(e)
            raise e
                    
        
    
    def text_to_audio(self, text, voice="onyx", model="tts-1", _retrie=False):
        try:
            audioResponse = self.client.audio.speech.create(
                model=model,
                voice=voice,
                input=text,
                response_format="wav",
            )
        except (openai.APIConnectionError or openai.InternalServerError or openai.UnprocessableEntityError) as e:
            if _retrie:
                raise e
            tts_partial = partial(self.text_to_audio, text, voice, model)
            ChatGPT.__error_handling(tts_partial)
        except openai.APIError as e:
            print("Text to Audio Api call failed!")
            print(e)
            raise e
            
        
        self.write_audio_to_file(audioResponse)
        
        return True
        
    
    def audio_to_text(self, prompt="", model ="whisper-1", _retrie=False):   
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
        except OSError as e: 
            print(f"Failed to open file {self.file_user_input}")
            print(e)
            raise e
        except (openai.APIConnectionError or openai.InternalServerError or openai.UnprocessableEntityError) as e:
            if _retrie:
                raise e
            stt_partial = partial(self.audio_to_text, prompt, model)
            return ChatGPT.__error_handling(stt_partial)  
        except openai.APIError as e:
            print("Audio to text Api call failed!")
            print(e)
            raise e
        
    
    def get_user_audio(self, duration=10):
        samplerate = 44100 
        
        print("Speak now...")
        
        try:
            data = sd.rec(int(samplerate * duration), samplerate, channels=2)

            while duration > 0:
                print(duration)
                duration = duration - 1
                time.sleep(1)

            sd.wait()

            print("Recording finished!")


            wavWrite(self.file_user_input, samplerate, data) 
        except OSError as e: 
            print("Failed to recored audio!")
            print(e)
            raise e
        
    
    def write_audio_to_file(self, audio_data):
        try:
            with open(self.file_tts_out, "wb") as audio_file:
                for chunk in audio_data.iter_bytes(chunk_size=1024):
                    if chunk:
                        audio_file.write(chunk)
        except OSError as e: 
            print(f"Failed to write to audio file!")
            print(e)
            raise e
        
        
    def construct_message(self, userInput, system_prompt):
        #format user and system prompt for api 
        system_prompt = {"content": system_prompt, "role": "system"}
            
        self.set_history("user" , userInput)
        
        #construct message for api call 
        message = []
        message.append(system_prompt)
        message.extend(self._history)
        
        return message  

    
    def set_history(self, role, value):
        self._history.append({"content": value, "role": role})
        
        if len(self._history) >= self.max_length * 2:
            del self._history[0]
            del self._history[0]  
   
   
    @staticmethod
    def __error_handling(method):
        count = 0
       
        while count < 3:
            try:
                result = method()
                return result
            except openai.APIError as e: 
                count += 1
                exception = e
            except OSError as e:
                raise e
            
            time.sleep(3)
        
        raise exception
    
                  
    def __TTS_test(self, text=None):
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