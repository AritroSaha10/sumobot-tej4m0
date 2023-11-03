import bluetooth
from controller import Controller
import time

if __name__ == "__main__":
    serial_port = bluetooth.initialize_bluetooth_serial()
    controller = Controller(0)

    print("Running!")
    running: bool = True
    while running:
        if not controller.loop():
            running = False

        drive_state = controller.drive_state
        if drive_state is not None:
            print(drive_state.format_for_device())
            serial_port.write(drive_state.format_for_device())
            serial_port.flush()

            # Keep delay to not overload serial port
            time.sleep(0.025)
    
    serial_port.close()
        