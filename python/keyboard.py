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

    def convert_to_drivestate(self) -> DriveState:
        return DriveState(
            throttle=(self.key_w * 255 + self.key_s * 255), 
            turn=(self.key_d * 255 + self.key_a * -255)
        )

class Keyboard(InputDevice):
    _keyboard_state: KeyboardState

    def __init__(self):
        super()

        
