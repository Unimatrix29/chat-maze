from Color import Color
import pygame

class Screen():
    
    def __init__(self, maze, screenNumber=0,):
        
        pygame.init()
        
        self.displaySizeX, self.displaySizeY = pygame.display.get_desktop_sizes()[screenNumber]
        self.display = pygame.display.set_mode((self.displaySizeX, self.displaySizeY), display=screenNumber)
        
        self.cellSpacing = 5
        self.borderWidth = 2
        textSize = 36
        
        self.currentMaze = maze
        
        self.cellSize = self.__calculateCellSize()
        self.mazeBorder = self.__calculateMazeBorder()
        self.chatBorder = self.__calculateChatBorder(textSize)
        
        self.text = ''
        self.font = pygame.font.Font(None, textSize)
          
        
    def update(self):
        
        self.display.fill(Color.BACKGROUND.value)
        
        self.__drawMazeBorder()
        self.__drawChatBorder()
        
        self.__drawMaze()
        
        self.__getUserInput()
        self.__drawUserInput()
        
        
        pygame.display.flip()
        
        
    def __drawMaze(self, color=Color.MAZE_CELL.value): 
        # Iterate through the maze and draw each cell
        for x in range(0, len(self.currentMaze)):
            for y in range(0, len(self.currentMaze)):
                # Calculate the position and size of each cell
                rect = pygame.Rect(0, 0, self.cellSize, self.cellSize)
                rect.x = x * self.cellSize + self.cellSpacing * (x + 1) + self.borderWidth
                rect.y = y * self.cellSize + self.cellSpacing * (y + 1) + (self.displaySizeY - self.displaySizeX/2)/2 + self.borderWidth
            
                # Draw the cell with the corresponding color
                pygame.draw.rect(self.display, color, rect, self.currentMaze[y][x] -1)


    
    
    def __drawMazeBorder(self, color=Color.MAZE_BORDER.value):
        # Draw the maze border
        pygame.draw.rect(self.display, color, self.mazeBorder, width=self.borderWidth)            
          
                
    def __calculateMazeBorder(self):
        # Create a border for the maze
        border = pygame.Rect(0,0,0,0)
        border.width = self.displaySizeX/2
        border.height = border.width
        border.center = (self.displaySizeX/4, self.displaySizeY/2)
        
        return border
    
    
    def __calculateCellSize(self):
        cellSize = (self.displaySizeX/2 - self.cellSpacing * (len(self.currentMaze) + 1) - self.borderWidth * 2) / len(self.currentMaze)
        
        return cellSize             
    

    def __getUserInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif self.font.size(self.text + event.unicode)[0] + self.font.size("A")[0]/3 < self.chatBorder.width:
                    if event.unicode.isprintable():
                        self.text += event.unicode
                else:
                    pass
    
    
    def __drawUserInput(self, color=Color.TEXT.value):
        textSurface = self.font.render(self.text, True, color)
        self.display.blit(textSurface, (self.chatBorder.x + self.font.size("A")[0]/3, self.chatBorder.y + self.chatBorder.height / 2 - self.font.get_height() / 2))
    
    
    def __calculateChatBorder(self, size):
        padding = self.cellSize
        
        border = pygame.Rect(0,0,0,0)                
        border.width = self.displaySizeX/2 - padding * 2
        border.height = size
        border.x = self.displaySizeX/2 + padding
        border.y = self.mazeBorder.y + self.mazeBorder.height - border.height
        
        return border
    
    
    def __drawChatBorder(self, color=Color.CHAT_BORDER.value):
        pygame.draw.rect(self.display, color, self.chatBorder, width=self.borderWidth)