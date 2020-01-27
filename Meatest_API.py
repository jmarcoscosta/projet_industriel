import serial
from tkinter import messagebox



class Meatest:
    name = "meatest"
    def write(self,command_text):
        b = bytes(command_text + "\n", 'utf-8')  # on transforme la chaine str en byte
        # print(command_text+"\n")
        communication.write(b)

    def setup_communication(self):

        import serial.tools.list_ports

        print('Searching...')
        ports = serial.tools.list_ports.comports(include_links=False)
        for port in ports:
            print('Port found:' + port.device)

        global communication
        communication = serial.Serial(
        port = ports[0].device,
        baudrate = 19200,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        xonxoff = True,
        timeout = 1
        )
        if communication.isOpen():
            print("Device Connected")
            communication.flushInput()
            communication.flushOutput()
            self.write("*REM <lf>")
            self.write("OUTP ON <lf>")
        else:
            messagebox.showinfo("Serial Communication", "Device Not Connected")
            return 0
    def close_communication(self):
        if communication.isOpen():
            print("Closing communication...")
            communication.flushInput()
            communication.flushOutput()
            self.dc_tension_output(0,"mv")
            self.write("OUTP OFF <lf>")
            self.write("*LOC <lf>")
            communication.close()


    def ac_tension_output(self,value,frequency_Hz,unit):
        VAC_range = {
            "MV": 1e-3,
            "V": 1
        }
        value_ = value*VAC_range[unit.upper()]
        command_text = "FUNC"+" SIN;:VOLT "+str(value_)+";:FREQ "+str(frequency_Hz)+"<lf>"
        print(command_text)
        self.write(command_text)

    def dc_tension_output(self,value,unit):
        VDC_range = {
            "MV": 1e-3,
            "V": 1
        }
        # print(type(value))
        # print(type(VDC_range[unit.upper()]))
        value_ = value*VDC_range[unit.upper()]
        command_text = "FUNC"+" DC;:VOLT "+str(value_)+"<lf>"
        # print(command_text)
        self.write(command_text)



    def ac_current_output(self,value,frequency_Hz,unit):
        IAC_range = {
            "UA": 1e-6,
            "MA": 1e-3,
            "A": 1
        }
        value_ = value*IAC_range[unit.upper()]
        command_text = "FUNC"+" SIN;:CURR "+str(value_)+";:FREQ "+str(frequency_Hz)+"<lf>"
        # print(command_text)
        self.write(command_text)


    def dc_current_output(self,value,unit):
        IDC_range = {
            "UA": 1e-6,
            "MA": 1e-3,
            "A": 1
        }
        value_ = value*IDC_range[unit.upper()]
        command_text = "FUNC"+" DC;:CURR "+str(value_)+"<lf>"
        self.write(command_text)

    def resistance_output(self,value, unit):
        R_range = {
            "O": 1,
            "KO": 1e3,
            "MO": 1e6
        }
        value_ = value*R_range[unit.upper()]
        command_text = "RES "+str(value_)+"<lf>"
        self.write(command_text)












