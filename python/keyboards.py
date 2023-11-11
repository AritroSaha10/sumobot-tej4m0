import dataclasses
import pygame

from drivestate import DriveState
from inputdevice import InputDevice

@dataclasses.dataclass
class KeyboardState: 
    key_w: bool
    key_s: bool
    key_a: bool
    key_d: bool

    key_esc: bool

    def convert_to_drivestate(self) -> DriveState:
        return DriveState(
            throttle=(self.key_w * 255 + self.key_s * -255), 
            turn=(self.key_d * 255 + self.key_a * -255)
        )

class Keyboard(InputDevice):
    keyboard = pygame.key
    _keyboard_state: KeyboardState

    def __init__(self):
        super().__init__()

        self.width = 500
        self.height = 500
        self.colour = (255, 255, 255)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(self.colour)

        self.font = pygame.font.SysFont("arial", 20)
        self.text = self.font.render("Keep This Window Focused", True, (0, 0, 0), (255, 255, 255))
        self.textRect = self.text.get_rect()
        self.textRect.center = self.width//2, self.height//2

        self.screen.blit(self.text, self.textRect)

        pygame.display.flip()
        
    def loop(self) -> bool:
        self._keyboard_state = self._get_keyboard_state()

        if self._keyboard_state.key_esc:
            self.exit()
            return False    

        return super().loop()

    @property
    def keyboard_state(self):
        return self._keyboard_state
    
    @property
    def drive_state(self):
        return self._keyboard_state.convert_to_drivestate()
    
    def _get_keyboard_state(self):
        _pygame_keyboard_state = self.keyboard.get_pressed() 
        return KeyboardState(
            key_w = _pygame_keyboard_state[pygame.K_w],
            key_s = _pygame_keyboard_state[pygame.K_s],
            key_a = _pygame_keyboard_state[pygame.K_a],
            key_d = _pygame_keyboard_state[pygame.K_d],
            key_esc = _pygame_keyboard_state[pygame.K_ESCAPE]
        )
        
