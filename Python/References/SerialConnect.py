import serial.tools.list_ports

def serial_ports():

    # produce a list of all serial ports. The list contains a tuple with the port number, 
    # description and hardware address
    #
    ports = list(serial.tools.list_ports.comports())  

    # return the port if 'USB' is in the description 
    for port_no, description, address in ports:
        if 'Arduino' in description:
            port_no = str(port_no)
            print(port_no)


serial_ports()