# API for Fluke 5500 and 5520 (RS 232)
import serial
from tkinter import messagebox

class Fluke:
    name = "fluke"
    def setup_communication(self):
        import serial.tools.list_ports
        print('Searching...')
        ports = serial.tools.list_ports.comports(include_links=False)
        for port in ports:
            print('Port found:' + port.device)

        global communication
        communication = serial.Serial(
        port = ports[0].device,
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        xonxoff = True,
        timeout = 1
        )
        if communication.isOpen():
            # messagebox.showinfo("Serial Communication", "Device Connected")
            print("Device Connected")
            communication.flushInput()
            communication.flushOutput()

    def close_communication(self):
        if communication.isOpen():
            print("Closing communication...")
            communication.flushInput()
            communication.flushOutput()
            self.dc_tension_output(0,"mv")
            communication.close()

    def write(self,command_text):
        # print("write called")
        b = bytes(command_text+"\n", 'utf-8')  # on transforme la chaine str en byte
        # print(command_text+"\n")
        communication.write(b)


    def ac_tension_output(self,value, frequency_hz, unit):
        command_text = "OUT "+str(value)+" "+unit.upper()+" , "+str(frequency_hz)+" HZ"
        command_text += " ; OPER "
        # print(command_text)
        self.write(command_text)

    def dc_tension_output(self,value, unit):
        # print("dc fluke")
        command_text = "OUT "+str(value)+" "+unit.upper()+" , 0 HZ"
        command_text += " ; OPER "
        # print(command_text)
        self.write(command_text)


    def ac_current_output(self,value, frequency_hz, unit):
        command_text = "OUT "+str(value)+" "+unit.upper()+" , "+str(frequency_hz)+" HZ"
        command_text += " ; OPER "
        # print(command_text)
        self.write(command_text)


    def dc_current_output(self,value, unit):
        command_text = "OUT "+str(value)+" "+unit.upper()+" , 0 HZ"
        command_text += " ; OPER "
        # print(command_text)
        self.write(command_text)


    def resistance_output(self,value, unit):
        R_range = {
            "O": 1,
            "KO": 1e3,
            "MO": 1e6
        }
        value_ = value*R_range[unit.upper()]
        command_text = "OUT "+str(value_)+" OHM"
        command_text += " ; OPER "
        # print(command_text)
        self.write(command_text)
















