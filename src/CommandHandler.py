from pathlib import Path
import json

class Command():
    
    def __init__(self, game):
        self.game = game
        self.chatgpt = self.game.chatgpt

        #self.chatgpt = chatgpt
        
        self.info_txt = "This is a info text, it texts infos"
        self.command_list = "This is a help texts , it texts hepls"
        self.help_prompt = "Du bekommst einen Text übergeben. Bitte fass ihn in drei Sätzen zusammen."
        self.quack_txt = "quack"
        
        self.__get_command_txt_from_json()
        
        self.commands = {
            "/help"      :   self.__help,
            "/info"      :   self.__info,
            "/newgame"     :   self.__newgame,
            "/restart"   :   self.__restart,
            "/clear"     :   self.__clear,
            #"/difficulty":   self.__difficulty,
            "/audio on"  :   self.__audio_on,
            "/audio off" :   self.__audio_off,
            "/quack"     :   self.__quack   
        }
        
        
    def execute(self, input):
        command = self.commands.get(input.lower().strip(), None)

        if command == None:
            return False
        
        command()
        
        return True
    
    
    def __help(self):
        help_txt_combined = f"{self.__get_help_txt()}\n{self.command_list}"
        print(help_txt_combined)
        self.game.screen.add_chat_text(help_txt_combined, "System")
    
    
    def __info(self):
        self.game.screen.add_chat_text(self.info_txt, "System")
    
    
    def __newgame(self):
        self.game.reset()
        
    
    def __restart(self):
        self.game.restart()
    
    
    def __clear(self):
        self.game.screen.clear_chat_text()
    
    #obsolete
    def __difficulty(self):
        split_user_input = self.game.screen.get_user_input().strip().split(" ")
        try:
            level = int(split_user_input[1])
        except ValueError: 
            self.game.screen.add_chat_text("Please enter /difficulty followed by a number between 1-3 to change the difficulty.", "System")
            return None
        
        self.game.gameHandler.set_level(level)
    
    
    def __audio_on(self):
        self.game.audio_event.set()
    
    
    def __audio_off(self):
        self.game.audio_event.clear()
    
    
    def __quack(self):
        self.game.screen.add_chat_text(self.quack_txt, "System")
    
    
    def __get_command_txt_from_json(self):
        display_texts_file = Path(__file__).parent / "command_texts.json"
        display_texts_file.resolve()
        
        try:
            with open(display_texts_file, "r") as file:
                data = json.load(file)
                
                self.command_list = data["help_text"]
                self.info_txt = data["info_text"]
                self.help_prompt = data["help_prompt"]
                self.quack_txt = data["quack_text"]
        except FileNotFoundError as e: 
            print("display_texts.json was not found")
            print(e)
        except json.JSONDecodeError as e: 
            print("There was an Erorr while decoding display_texts.json")
            print(e)
        except OSError as e: 
            print("There was an Erorr while reading a File")
            print(e)
        
    def __get_help_txt(self):
        
        message = self.game.chatgpt.construct_message(userInput=self.game.prompt, system_prompt=self.help_prompt)
        print(message)
        chat_response = self.game.chatgpt.text_to_text(message=message, model="gpt-4o")
        
        content = chat_response.choices[0].message.content
        
        return content