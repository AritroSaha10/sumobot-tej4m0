import pygame
import pygame._sdl2.controller as pg_sdl_controller
import sys
import dataclasses
import math
from drivestate import DriveState
from inputdevice import InputDevice

DEADZONE = 15

# https://www.desmos.com/calculator/diehz25nfg
def transform_joystick_axis(raw: float, reflect: bool = False) -> int:
    return int((raw / abs(raw)) * math.sqrt(abs(x)) * 255) * (-1 if reflect else 1)

@dataclasses.dataclass
class ControllerState:
    left_stick_x: float
    left_stick_y: float
    left_trigger: float

    right_stick_x: float
    right_stick_y: float
    right_trigger: float

    button_a: bool
    button_b: bool
    button_x: bool
    button_y: bool

    button_ls: bool
    button_rs: bool
    
    def convert_to_drive_state(self) -> DriveState:
        return DriveState(
            throttle = transform_joystick_axis(self.left_stick_y, True),
            turn = transform_joystick_axis(self.right_stick_x, False)
        )

class Controller(InputDevice):
    joystick: pg_sdl_controller.Controller
    _controller_state: ControllerState

    def __init__(self, joystick_id: int):
        super().__init__()
        
        # Initialize joystick
        pygame.joystick.init()
        pg_sdl_controller.init()

        # Check for joystick count
        if pygame.joystick.get_count() < max(0, joystick_id + 1):
            raise AttributeError("No Controller Detected")

        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        self.joystick = pg_sdl_controller.Controller.from_joystick(joystick)

    def loop(self) -> bool:
        self._controller_state = self._get_joystick_state()

        if self._controller_state.button_ls and self._controller_state.button_rs:
            self.exit()
            return False

        return super().loop()

    @property
    def controller_state(self):
        return self._controller_state
    
    @property
    def drive_state(self):
        return self._controller_state.convert_to_drive_state()

    def _get_joystick_state(self):
        return ControllerState(
            left_stick_x=self.joystick.get_axis(pygame.CONTROLLER_AXIS_LEFTX) / 32768,
            left_stick_y=self.joystick.get_axis(pygame.CONTROLLER_AXIS_LEFTY) / 32768,
            right_stick_x=self.joystick.get_axis(pygame.CONTROLLER_AXIS_RIGHTX) / 32768,
            right_stick_y=self.joystick.get_axis(pygame.CONTROLLER_AXIS_RIGHTY) / 32768,
            left_trigger=self.joystick.get_axis(pygame.CONTROLLER_AXIS_TRIGGERLEFT) / 32768,
            right_trigger=self.joystick.get_axis(pygame.CONTROLLER_AXIS_TRIGGERRIGHT) / 32768,
            button_a=self.joystick.get_button(pygame.CONTROLLER_BUTTON_A),
            button_b=self.joystick.get_button(pygame.CONTROLLER_BUTTON_B),
            button_x=self.joystick.get_button(pygame.CONTROLLER_BUTTON_X),
            button_y=self.joystick.get_button(pygame.CONTROLLER_BUTTON_Y),
            button_ls=self.joystick.get_button(pygame.CONTROLLER_BUTTON_LEFTSTICK),
            button_rs=self.joystick.get_button(pygame.CONTROLLER_BUTTON_RIGHTSTICK),
        )
