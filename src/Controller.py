import random 
import pygame, sys

class Controller():

    def __init__(self):
        pass

    def setup_screen(self):
        pygame.init()
        #self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode([800, 200])
        pygame.display.set_caption("text_input")
        self.base_font = pygame.font.Font(None, 32)
        self.user_text = ""

        self.input_rect = pygame.Rect(10, 10, 140, 32)
        self.color_active = pygame.Color('limegreen')
        self.color_passive = pygame.Color('gray15')
        self.color = self.color_passive

        self.active = True
        self.return_text = False
        self.message = ""

    def update_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_rect.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        self.return_text = True
                        self.message = self.user_text
                        self.user_text = ""
                        break
                    elif event.key == pygame.K_BACKSPACE:
                        self.user_text = self.user_text[:-1]
                    else:
                        self.user_text += event.unicode

            self.screen.fill((0,0,0))

            if self.active:
                self.color = self.color_active
            else:
                self.color = self.color_passive

            pygame.draw.rect(self.screen, self.color, self.input_rect, 2)
            self.text_surface = self.base_font.render(self.user_text, True, (255,255,255))
            self.screen.blit(self.text_surface,(self.input_rect.x + 5, self.input_rect.y + 5))
            self.input_rect.w = max(10, self.text_surface.get_width() + 10)
            pygame.display.flip()
            #clock.tick(60)

    def get_user_input(self):
        return self.message
    
    def on_return(self):
        if self.return_text:
            self.return_text = False
            return True
        return False
    



    



        
