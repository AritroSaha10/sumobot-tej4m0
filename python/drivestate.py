import dataclasses

@dataclasses.dataclass
class DriveState:
    throttle: float
    turn: float 

    def format_for_device(self) -> bytes:
        state_str = f"{self.throttle},{self.turn}\n"
        return bytes(state_str, "ascii")