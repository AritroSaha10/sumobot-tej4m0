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
    elif sys.platform.startswith("darwin"):
        serial_port_name_key = "cu.HC-06"
        print("WARNING: MacOS support is experimental due to bluetooth serial issues on Darwin platforms. Please consider using a Windows or Linux computer instead.")
    else:
        raise OSError("OS not supported yet")

    print("\nScanning for serial ports...\n")
    serial_port = None
    valid_ports = [port for port in ports if serial_port_desc_key in port.description and serial_port_name_key in port.name]

    for port in valid_ports:
        try:
            print(f"attempting port {port.device}...")

            tmp_serial = serial.Serial(port.device, 57600, timeout = 1) #Change your port name COM... and your baudrate
            tmp_serial.write_timeout = 2
            if input("Is the LED of the bluetooth module currently solid? (y/n) ") == "y":
                serial_port = tmp_serial
                print(f"port {port.name} is valid!")
                break
            else:
                print(f"port {port.name} incorrect...")
                tmp_serial.close()
                continue
        except SerialException as e:
            print(f"port {port.name} invalid...", e)
        
        print()


    assert serial_port is not None, "Could not find valid serial port"
    return serial_port

