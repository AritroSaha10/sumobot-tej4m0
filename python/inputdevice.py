import pygame
from abc import ABC, abstractmethod


class InputDevice(ABC):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 400))

        self.font = pygame.font.SysFont("comicsansms", 20)

        self.text = self.font.render("Keep Window Focused", True, (0, 0, 0), (255, 255, 255))
    
    @abstractmethod
    def loop(self) -> bool:
        for game_event in pygame.event.get():
            if game_event.type == pygame.QUIT:
                self.exit()
                return False
        
        self.screen.fill((255, 255, 255))

        self.screen.blit(self.text, (100,  150))
        pygame.display.flip()
        # Limit loop to 60 Hz
        pygame.time.Clock().tick(60)
        
        return True
     
    @property
    @abstractmethod
    def drive_state(self):
        pass
    
    def exit(self):
        pygame.quit()