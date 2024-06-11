class Command():
    
    def __init__(self, screen, gameHandler, player, game):
        self.screen = screen
        self.gameHandler = gameHandler
        self.player = player
        self.game = game
        #self.chatgpt = chatgpt
        
        
        self.info_txt = "This is a info text, it texts infos."
        self.help_txt = "This is a help texts , it texts hepls"
        
        self.commands = {
            "help"      :   self.__help,
            "info"      :   self.__info,
            "reset"     :   self.__reset,
            "clear"     :   self.__clear,
            "difficulty":   self.__difficulty,
            "audio on"  :   self.__audio_on,
            "audio off" :   self.__audio_off
        }
        
        
    def get(self, input):
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
        
    