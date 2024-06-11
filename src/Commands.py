from pathlib import Path
import json

class Command():
    
    def __init__(self, screen, gameHandler, player, game):
        self.screen = screen
        self.gameHandler = gameHandler
        self.player = player
        self.game = game
        #self.chatgpt = chatgpt
        
        self.info_txt = ""
        self.help_txt = "This is a help texts , it texts hepls"
        
        self.help_prompt = ""
        
        self.__get_command_txt_from_json()
        
        

        
        self.commands = {
            "help"      :   self.__help,
            "info"      :   self.__info,
            "reset"     :   self.__reset,
            "clear"     :   self.__clear,
            "difficulty":   self.__difficulty,
            "audio on"  :   self.__audio_on,
            "audio off" :   self.__audio_off
        }
        
        
    def execute(self, input):
        command = self.commands.get(input.lower().strip(), None)

        if command == None:
            return False
        
        command()
        
        return True
    
    
    def __help(self):
        self.screen.response_text = self.help_txt
    
    
    def __info(self):
        self.screen.response_text = self.info_txt
    
    
    def __reset(self):
        self.game.restart()
    
    
    def __clear(self):
        pass
    
    
    def __difficulty(self):
        pass
    
    
    def __audio_on(self):
        pass
    
    
    def __audio_off(self):
        pass
    
    
    def __get_command_txt_from_json(self):
        display_texts_file = Path(__file__).parent / "command_texts.json"
        display_texts_file.resolve()
        
        try:
            with open(file, "r") as file:
                data = json.load(file)
                
                self.info_txt = data["info_text"]
                self.help_prompt = data["help_prompt"]
        except FileNotFoundError as e: 
            print("display_texts.json was not found")
            print(e)
        except json.JSONDecodeError as e: 
            print("There was an Erorr while decoding display_texts.json")
            print(e)
        except OSError as e: 
            print("There was an Erorr while reading a File")
            print(e)
        
    