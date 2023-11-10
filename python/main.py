import bluetooth
from controller import Controller
from inputdevice import InputDevice
import time

if __name__ == "__main__":
    serial_port = bluetooth.initialize_bluetooth_serial()
    
    inp_device: InputDevice = None
    try:
        inp_device = Controller(0)
    except AttributeError:
        print("Controller not connected, falling back to keyboard")

    print("Running!")
    running: bool = True
    while running:
        if not inp_device.loop():
            running = False

        drive_state = inp_device.drive_state
        if drive_state is not None:
            print(drive_state.format_for_device())
            serial_port.write(drive_state.format_for_device())
            serial_port.flush()

            # Keep delay to not overload serial port
            time.sleep(0.025)
    
    serial_port.close()