import serial
from serial.serialutil import SerialException
import sys
import serial.tools.list_ports

def initialize_bluetooth_serial() -> serial.Serial:
    ports = serial.tools.list_ports.comports()

    serial_port_key = ""
    if sys.platform.startswith("win"):
        serial_port_key = "Standard Serial over Bluetooth link"
    else:
        raise OSError("OS not supported yet")

    print("Scanning for serial ports...")
    serial_port = None
    valid_ports = [port for port in ports if serial_port_key in port.description]

    for port in valid_ports:
        try:
            tmp_serial = serial.Serial(port.name, 9600, timeout = 1) #Change your port name COM... and your baudrate

            if input("Is the LED of the bluetooth module currently solid? (y/n) ") == "y":
                serial_port = tmp_serial
                print(f"port {port.name} is valid!")
                break
            else:
                print(f"port {port.name} incorrect...")
                tmp_serial.close()
                continue
        except SerialException:
            print(f"port {port.name} invalid...")
            continue
        

    assert serial_port is not None, "Could not find valid serial port"
    return serial_port

