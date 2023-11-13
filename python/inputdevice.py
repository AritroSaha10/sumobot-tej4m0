import pygame
from abc import ABC, abstractmethod


class InputDevice(ABC):
    def __init__(self):
        pygame.init()
    
    @abstractmethod
    def loop(self) -> bool:
        for game_event in pygame.event.get():
            if game_event.type == pygame.QUIT:
                self.exit()
                return False
        
        # Limit loop to 60 Hz
        pygame.time.Clock().tick(60)
        
        return True
     
    @property
    @abstractmethod
    def drive_state(self):
        pass
    
    def exit(self):
        pygame.quit()