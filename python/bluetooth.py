import serial
from serial.serialutil import SerialException
import sys
import serial.tools.list_ports

def initialize_bluetooth_serial() -> serial.Serial:
    ports = serial.tools.list_ports.comports()

    serial_port_desc_key = ""
    serial_port_name_key = ""
    if sys.platform.startswith("win"):
        serial_port_desc_key = "Standard Serial over Bluetooth link"
    elif sys.platform.startswith("linux"):
        serial_port_name_key = "rfcomm"
    else:
        raise OSError("OS not supported yet")

    print("Scanning for serial ports...")
    serial_port = None
    valid_ports = [port for port in ports if serial_port_desc_key in port.description or serial_port_name_key in port.name]

    for port in valid_ports:
        try:
            tmp_serial = serial.Serial(port.device, 9600, timeout = 1) #Change your port name COM... and your baudrate

            if input("Is the LED of the bluetooth module currently solid? (y/n) ") == "y":
                serial_port = tmp_serial
                print(f"port {port.name} is valid!")
                break
            else:
                print(f"port {port.name} incorrect...")
                tmp_serial.close()
                continue
        except SerialException as e:
            print(f"port {port.name} invalid...")
            continue


    assert serial_port is not None, "Could not find valid serial port"
    return serial_port

