import pygame
import pygame._sdl2.controller as pg_sdl_controller
import sys
import dataclasses
import math

DEADZONE = 15

# https://www.desmos.com/calculator/diehz25nfg
def transform_joystick_axis(raw: float, reflect: bool = False) -> int:
    return int((raw / abs(raw)) * math.sqrt(abs(x)) * 255) * (-1 if reflect else 1)

@dataclasses.dataclass
class DriveState:
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

    def format_for_device(self) -> bytes:
        throttle = transform_joystick_axis(self.left_stick_y, True)
        turn = transform_joystick_axis(self.right_stick_x, False)
        if abs(throttle) < DEADZONE:
            throttle = 0
        if abs(turn) < DEADZONE:
            turn = 0

        state_str = f"{throttle},{turn}\n"
        return bytes(state_str, 'ascii')


class Controller:
    joystick: pg_sdl_controller.Controller
    _drive_state: DriveState

    def __init__(self, joystick_id: int):
        # Initialize Pygame and the joystick
        pygame.init()
        pygame.joystick.init()
        pg_sdl_controller.init()

        # Check for joystick count
        if pygame.joystick.get_count() < max(0, joystick_id + 1):
            print("Requested joystick not detected!")
            pygame.quit()
            sys.exit()

        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        self.joystick = pg_sdl_controller.Controller.from_joystick(joystick)

    def loop(self) -> bool:
        for game_event in pygame.event.get():
            if game_event.type == pygame.QUIT:
                self.exit()
                return False

        self._drive_state = self._get_joystick_state()

        if self._drive_state.button_ls and self._drive_state.button_rs:
            self.exit()
            return False

        # Limit loop to 60 Hz
        pygame.time.Clock().tick(60)

        return True

    @property
    def drive_state(self):
        return self._drive_state

    def _get_joystick_state(self):
        return DriveState(
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

#        return DriveState(
#            left_stick_x=self.joystick.get_axis(0),
#            left_stick_y=self.joystick.get_axis(1),
#            right_stick_x=self.joystick.get_axis(2),
#            right_stick_y=self.joystick.get_axis(3),
#            left_trigger=self.joystick.get_axis(4),
#            right_trigger=self.joystick.get_axis(5),
#            button_a=self.joystick.get_button(0),
#            button_b=self.joystick.get_button(1),
#            button_x=self.joystick.get_button(2),
#            button_y=self.joystick.get_button(3),
#            button_ls=self.joystick.get_button(8),
#            button_rs=self.joystick.get_button(9),
#        )

    def exit(self):
        pygame.quit()
