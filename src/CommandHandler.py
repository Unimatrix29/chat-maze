from pathlib import Path
import json

class Command():
    
    def __init__(self, game):
        self.game = game
        self.chatgpt = self.game.chatgpt
        
        self.info_txt = "This is a info text, it texts infos"
        self.command_list = "This is a help texts , it texts hepls"
        self.help_txt = {"placeholder" : "This is a help text, it texts helps"}
        self.welcome_txt = "Text to show at the start screen"
        self.start_txt = "Text to show after a game has started"
        self.end_txt = "Text to show after a game is finished"
        self.help_prompt = "Du bekommst einen Text übergeben. Bitte fass ihn in drei Sätzen zusammen."        
        self.quack_txt = "quack"
        
        self.__get_command_txt_from_json()
        
        self.commands = {
            "/help"      :   self.__help,
            "/info"      :   self.__info,
            "/newgame"   :   self.__newgame,
            "/restart"   :   self.__restart,
            "/clear"     :   self.__clear,
            "/commands"  :   self.__commands,
            "/audio on"  :   self.__audio_on,
            "/audio off" :   self.__audio_off,
            "/quack"     :   self.__quack,
            "__/start"   :   self.__print_start_message,
            "__/finish"  :   self.__print_end_message
        }
        
        self.__print_welcome_message()
        
    def execute(self, input):
        command = self.commands.get(input.lower().strip(), None)

        if command == None:
            return False
        
        command()
        
        return True
    
    
    def __help(self):
        promptKey = self.game.prompt[0]
        self.game.screen.add_chat_text(self.help_txt.get(promptKey), "System")
        self.__commands()
    
    def __info(self):
        self.game.screen.add_chat_text(self.info_txt)
    
    
    def __newgame(self):
        self.__print_welcome_message()
        self.game.reset()
        self.game.screen.add_chat_text(self.start_txt)
        
    
    def __restart(self):
        self.game.restart()
        self.game.screen.add_chat_text(self.start_txt)
    
    
    def __clear(self):
        self.game.screen.clear_chat_text()
        
    
    def __commands(self):
        self.game.screen.add_chat_text(self.command_list, "System")
    
    
    def __audio_on(self):
        self.game.audio_event.set()
        self.game.screen.add_chat_text("Drücke STRG und Lehrtaste zum sprechen", "System")

    
    def __audio_off(self):
        self.game.audio_event.clear()
        self.game.screen.add_chat_text("Die Spracheingabe ist nun deaktiviert", "System")
        

    def __print_welcome_message(self):
        self.__clear()
        self.game.screen.add_chat_text("      __  __     ______   __     __          ")
        self.game.screen.add_chat_text("     /\ \_\ \   /\__  _\ /\ \  _ \ \         ")
        self.game.screen.add_chat_text("     \ \  __ \  \/_/\ \/ \ \ \/ \".\ \       ")
        self.game.screen.add_chat_text("      \ \_\ \_\    \ \_\  \ \__/\".~\_\      ")
        self.game.screen.add_chat_text("       \/_/\/_/     \/_/   \/_/   \/_/       ")
        self.game.screen.add_chat_text("*********************************************")
        
        # self.game.screen.add_chat_text(" ************************** : *****", "***** ")
        # self.game.screen.add_chat_text("    Welcome to Chat Maze    : *****", "***** ")
        # self.game.screen.add_chat_text(" ************************** : *****", "***** ")

        self.game.screen.add_chat_text(self.welcome_txt)
    
    def __print_start_message(self):
        self.game.screen.add_chat_text(self.start_txt)

    def __print_end_message(self):
        self.game.screen.add_chat_text(" ########################## : #####", "##### ")
        self.game.screen.add_chat_text("      Congratulations!      : #####", "##### ")
        self.game.screen.add_chat_text(" ########################## : #####", "##### ")

        self.game.screen.add_chat_text(self.end_txt)
        self.__info()
    
    def __quack(self):
        self.game.screen.add_chat_text(self.quack_txt, "System")
    
    
    def __get_command_txt_from_json(self):
        display_texts_file = Path(__file__).parent / "command_texts.json"
        display_texts_file.resolve()
        
        try:
            with open(display_texts_file, "r") as file:
                data = json.load(file)
                
                self.info_txt = data["info_text"]
                self.command_list = data["command_list"]
                self.help_txt = data["help_text"]
                self.welcome_txt = data["welcome_text"]
                self.start_txt = data["start_text"]
                self.end_txt = data["end_text"]
                self.help_prompt = data["help_prompt"]
                self.quack_txt = data["quack_text"]
        except FileNotFoundError as e: 
            print("display_texts.json was not found")
            print(e)
        except json.JSONDecodeError as e: 
            print("There was an Erorr while decoding command_texts.json")
            print(e)
        except OSError as e: 
            print("There was an Erorr while reading a File")
            print(e)
        
    def __get_help_txt_from_chatgpt(self):
        
        message = self.game.chatgpt.construct_message(userInput=self.game.prompt, system_prompt=self.help_prompt)
        print(message)
        chat_response = self.game.chatgpt.text_to_text(message=message, model="gpt-4o")
        
        content = chat_response.choices[0].message.content
        
        return content