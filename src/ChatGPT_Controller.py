import openai, time, traceback
import numpy as np 
import sounddevice as sd
from pathlib import Path
from scipy.io.wavfile import write as wavWrite
from functools import partial

class ChatGPT():
    """
    The ChatGPT class provides methods to interact with OpenAI's GPT and audio models. 
    It includes functionalities for text-to-text, text-to-audio, and audio-to-text conversions, 
    as well as methods for handling user audio input and managing conversation history.

    Attributes
    -----------
        _client (object): The OpenAI client used for API calls.
        _history (list): A list to store the conversation history.
        _max_length (int): The maximum length of the conversation history.
        _file_tts_out (Path): The file path for the text-to-speech output.
        _file_user_input (Path): The file path for the user audio input.

    Methods
    -----------
        __init__(self, client, max_history_length=5):
            Initializes the ChatGPT instance with a client and optional maximum history length.

        text_to_text(self, message, temperature=1, model="gpt-3.5-turbo", _retrie=False):
            Sends a text message to the GPT model and returns the response.

        text_to_audio(self, text, name="onyx", model="tts-1", _retrie=False):
            Converts text to audio using the specified voice model and saves the audio file.

        audio_to_text(self, prompt="", model="whisper-1", _retrie=False):
            Converts audio input to text using the specified model.

        get_user_audio(self, duration=10):
            Records user audio for a specified duration and saves it to a file.

        write_audio_to_file(self, audio_data):
            Writes audio data to a file.

        construct_message(self, userInput, system_prompt):
            Constructs a message for the API call by formatting the user and system prompts as well as the conversation history.

        set_history(self, role, value):
            Adds a message to the conversation history and manages the history length.

        __error_handling(method):
            Static method for handling API errors with retries.

        __TTS_test(self, text=None):
            Tests the text-to-speech functionality by converting text to audio and playing it.
    """

    def __init__(self, client, max_history_length=5):
        """
        Initializes the ChatGPT instance with a client and optional maximum history length.

        Parameters
        ----------
        client : object
            The OpenAI client used for API calls.
        max_history_length : int, optional
            The maximum length of the conversation history. Defaults to 5.
        """
        
        self.client = client
        self._history = []
        self._max_length = max_history_length
        
        self._file_tts_out = Path(__file__).parent / "tts_out.wav"
        self._file_tts_out.resolve()
        self._file_user_input = Path(__file__).parent / "user_input.wav"
        self._file_user_input.resolve()

        if not self._file_tts_out.exists():
            self._file_tts_out.touch()
            

    def text_to_text(self, message, temperature=1, model="gpt-3.5-turbo", _retrie=False):
        """
        Sends a text message to the GPT model and returns the response.

        Parameters
        ----------
        message : list
            The message to be sent to the GPT model.
        temperature : float, optional
            The sampling temperature to use. Defaults to 1.
        model : str, optional
            The model to use for the API call. Defaults to "gpt-3.5-turbo".
        _retrie : bool, optional
            Internal parameter for retry logic. Defaults to False.

        Returns
        -------
        object
            The response from the GPT model.

        Raises
        ------
        openai.APIError
            If the API call fails.
        """
        
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
                    
        
    
    def text_to_audio(self, text, voice="Prinz Reginald", model="tts-1", _retrie=False):
        """
        Converts text to audio using the specified voice and model and saves the audio file.

        Parameters
        ----------
        text : str
            The text to be converted to audio.
        name : str, optional
            The name of the character to use. Defaults to "Prinz Reginald".
        model : str, optional
            The model to use for the API call. Defaults to "tts-1".
        _retrie : bool, optional
            Internal parameter for retry logic. Defaults to False.

        Raises
        ------
        openai.APIError
            If the API call fails.

        Returns
        -------
        bool
            True if the API call was successful.
        """
        
        # #map character names to voices
        # #for reference, see the OpenAI API documentation: https://platform.openai.com/docs/guides/text-to-speech/overview
        # voices={ "Prinz Reginald":"onyx", "Larry":"echo","Clyde":"shimmer","Lawrie":"fable", "Imane":"alloy","Sophia":"nova"}
        # voice = voices[name]
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
        """
        Converts audio input to text using the specified model.

        Parameters
        ----------
        prompt : str, optional
            An optional prompt to guide the transcription. Defaults to an empty string.
        model : str, optional
            The model to use for the API call. Defaults to "whisper-1" (currently there is only "whisper-1").
        _retrie : bool, optional
            Internal parameter for retry logic. Defaults to False.

        Raises
        ------
        openai.APIError
            If the API call fails.
        OSError
            If there is an issue with file operations.

        Returns
        -------
        str
            The transcribed text from the audio input.
        """
        
        try:
            with open(self._file_user_input, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model=model,
                    file=audio_file,
                    prompt=prompt,
                    language="de",
                    response_format="json"
                )
                
            return transcript.text
        except OSError as e: 
            print(f"Failed to open file {self._file_user_input}")
            print(e)
            traceback.print_exception(type(e), e, e.__traceback__)
            raise e.with_traceback(e.__traceback__)
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
        """
        Records user audio for a specified duration and saves it to a file.

        Parameters
        ----------
        duration : int, optional
            The duration for which to record audio, in seconds. Defaults to 10 seconds.

        Raises
        ------
        OSError
            If there is an issue with recording or saving the audio.
            
        Notes
        -----
        
        This method ist not used in the final implementation. It is provided for testing purposes.
        """
        
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


            wavWrite(self._file_user_input, samplerate, data) 
        except OSError as e: 
            print("Failed to recored audio!")
            print(e)
            traceback.print_exception(type(e), e, e.__traceback__)
            raise e.with_traceback(e.__traceback__)
        
    
    def write_audio_to_file(self, audio_data):
        """
        Writes audio data to a file.

        Parameters
        ----------
        audio_data : object
            The audio data to be written to the file.

        Raises
        ------
        OSError
            If there is an issue with writing to the file.
        """
        
        try:
            with open(self._file_tts_out, "wb") as audio_file:
                for chunk in audio_data.iter_bytes(chunk_size=1024):
                    if chunk:
                        audio_file.write(chunk)
        except OSError as e: 
            print(f"Failed to write to audio file!")
            print(e)
            traceback.print_exception(type(e), e, e.__traceback__)
            raise e.with_traceback(e.__traceback__)
        
        
    def construct_message(self, userInput, system_prompt):
        """
        Constructs a message for the API call by formatting the user and system prompts.

        Parameters
        ----------
        userInput : str
            The input provided by the user.
        system_prompt : str
            The system prompt to guide the conversation.

        Returns
        -------
        list
            A list of messages formatted for the API call.

        Notes
        -----
        This method formats the user and system prompts as well as the conversation history into a message structure suitable for the API call.
        For reference, see the OpenAI API documentation: https://platform.openai.com/docs/guides/chat-completions/getting-started
        It also updates the conversation history with the user input.
        """
        
        #format user and system prompt for api 
        system_prompt = {"content": system_prompt, "role": "system"}
            
        self.set_history("user" , userInput)
        
        #construct message for api call 
        message = []
        message.append(system_prompt)
        message.extend(self._history)
        
        return message  

    
    def set_history(self, role, value):
        """
        Adds a message to the conversation history.

        Parameters
        ----------
        role : str
            The role of the message, either "user" or "assistant".
        value : str
            The content of the message.

        Returns
        -------
        None
        
        Notes
        -----
        This method appends a new message to the conversation history with the specified role and content.
        If the history exceeds the maximum length, the oldest messages are removed to maintain the limit.
        """
    
        self._history.append({"content": value, "role": role})

        if len(self._history) >= self._max_length * 2:
            del self._history[0]
            del self._history[0]  
   
   
    @staticmethod
    def __error_handling(method):
        """
        Handles errors for API calls with retry logic.

        Parameters
        ----------
        method : function
            The method to be executed with retry logic.

        Raises
        ------
        openai.APIError
            If the method still fails after three attempts due to a openai.APIError.
        OSError
            If the method fails due to an `OSError`.

        Returns
        -------
        object
            The result of the method if successful.
            
        Notes
        -------
        This method attempts to execute the provided method up to three times in case of an `openai.APIError`.
        If the method fails due to an `OSError`, it raises the exception immediately.
        Between retries, it waits for 3 seconds.
        """
        
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
        """
        Test the text-to-speech functionality.
        Parameters
        ----------
        text : str, optional
            The text to be converted to audio. If not provided, a default test text will be used.
        Returns
        -------
        None
        
        Notes 
        -------
        This test uses the get_user_audio method to record audio input.
        """
        
        import pygame
        
        TTS = ChatGPT(self.client)

        pygame.mixer.init()
        
        if text == None:
            text = "Das ist der erste Test. Hier kommt gleich noch einer. Alle guten Dinge sind drei. Und weils so schön war hier noch ein vierter."

        TTS.text_to_audio(text)
        pygame.mixer.music.load(self._file_tts_out)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        pygame.mixer.music.unload()
