from tkinter import messagebox
from time import sleep

def file_startup(filename):
    file = open(filename, "w+")
    return file


def get_sequence_array(sequence):
    start = int(sequence[0])
    step = int(sequence[1])
    end = int(sequence[2])
    return start, step, end


def print_sequence(start, step, end, unit, frequency=0):
    for x in range(start, end + step, step):
        if frequency is 0:
            print(str(x) + " " + unit)
        else:
            print(str(x) + " " + unit + " " + str(frequency)+" Hz")


def parse_single_command(line):
    line_words = line.split()
    sequence_type = line_words[0]
    # VAC_50 5_V  # 2.5    -2.5  remplir    remplir   NOK

    if sequence_type == "VDC":
        tension = line_words[3]
        unit = line_words[1].split("_")[1]
        return sequence_type, float(tension), unit, 0

    elif sequence_type.startswith("VAC"):
        function = sequence_type.split('_')[0]
        frequency = sequence_type.split('_')[1]
        tension = line_words[3]
        unit = line_words[1].split("_")[1]
        print(tension)
        print(unit)
        print(function)
        print(frequency)
        # unit = line_words[3]
        # frequency = line_words[4]
        return function, float(tension), unit, frequency

    elif sequence_type == "IDC":
        current = line_words[3]
        unit = line_words[1].split("_")[1]
        # unit = line_words[3]
        return sequence_type, float(current), unit, 0

    elif sequence_type.startswith("IAC"):
        function = sequence_type.split('_')[0]
        frequency = sequence_type.split('_')[1]
        current = line_words[3]
        unit = line_words[1].split("_")[1]
        # unit = line_words[3]
        return function, float(current), unit, frequency

    elif sequence_type == "R":
        resistance = line_words[3]
        unit = line_words[1].split("_")[1]
        # unit = line_words[3]
        return sequence_type, float(resistance), unit, 0


def execute_sequence(API_function, start, step, end, unit, frequency=0):
    for module in range(start, end + step, step):
        if frequency is 0:
            API_function(module,unit)
        else:
            API_function(module,frequency, unit)


def execute_single_command(device,sequence_type, module, unit, frequency=0):
    # print("execute single command")
    # print(sequence_type)
    if sequence_type == "VDC":
        # print("sequence vdc")
        device.dc_tension_output(module, unit)
    elif sequence_type == "VAC":
        device.ac_tension_output(module, frequency, unit)
    elif sequence_type == "IDC":
        device.dc_current_output(module, unit)
    elif sequence_type == "IAC":
        device.ac_current_output(module, frequency, unit)
    elif sequence_type == "R":
        device.resistance_output(module, unit)

from tkinter.messagebox import askokcancel
def execute_sequence_file(device,filename,interface_output,acquisition):
    file = open(filename, "r")
    lines_list = file.readlines()
    previous_calib = "VDC_MV"

    for line in lines_list:
        # skip empty lines
        if not line.strip():
            continue
        line_words = line.split()
        function = line_words[0]

        functions = ["VDC","VAC","IDC","IAC","R"]
        # skip comments
        # if sequence_type[0] == "#":
        #     continue
        # elif sequence_type[0] == "-":
        if function[0:3] in functions:
            sequence_type, module, unit, frequency = parse_single_command(line)
            new_calib = sequence_type+"_"+unit.upper()

            if new_calib != previous_calib:
                # sleep(3)
                go_on = askokcancel("Changement de calibre","Passez au calibre "+new_calib+" "+str(module))

            previous_calib = new_calib
            if len(unit) == 1:
                acquisition_text = " ".join([sequence_type,str(module),unit,str(frequency)," Hz"])
            elif len(unit) ==2:
                acquisition_text = " ".join([sequence_type, str(module), unit[0].lower()+unit[1].upper(), str(frequency), " Hz"])
            interface_output(acquisition_text)
            execute_single_command(device,sequence_type,module,unit,frequency)
            sleep(0.5)
            acquisition(acquisition_text)
        # elif sequence_type == "VDC":
        #     sequence = line_words[1].split(":")
        #     start, step, end = get_sequence_array(sequence)
        #     unit = line_words[2]
        #     # print_sequence(start, step, end, unit)
        #     execute_sequence(device.dc_tension_output, start, step, end, unit)
        #
        # elif sequence_type == "VAC":
        #     sequence = line_words[1].split(":")
        #     start, step, end = get_sequence_array(sequence)
        #     unit = line_words[2]
        #     frequency = int(line_words[3])
        #     # print_sequence(start, step, end, unit, frequency)
        #     execute_sequence(device.ac_tension_output, start, step, end, unit, frequency)
        # elif sequence_type == "IDC":
        #     sequence = line_words[1].split(":")
        #     start, step, end = get_sequence_array(sequence)
        #     unit = line_words[2]
        #     # print_sequence(start, step, end, unit)
        #     execute_sequence(device.dc_current_output, start, step, end, unit)
        #
        # elif sequence_type == "IAC":
        #     sequence = line_words[1].split(":")
        #     start, step, end = get_sequence_array(sequence)
        #     unit = line_words[2]
        #     frequency = int(line_words[3])
        #     # print_sequence(start, step, end, unit, frequency)
        #     execute_sequence(device.ac_current_output, start, step, end, unit, frequency)
        #
        # elif sequence_type == "R":
        #     sequence = line_words[1].split(":")
        #     start, step, end = get_sequence_array(sequence)
        #     unit = line_words[2]
        #     # print_sequence(start, step, end, unit)
        #     execute_sequence(device.resistance_output, start, step, end, unit)
        elif function.startswith("FONCTION"):
            continue
        else:
            messagebox.showerror("ERROR", "Sequence type not found: "+line_words[0])
            return 0
        sleep(1)

def pop_up_R(root=0):
    from tkinter import simpledialog
    _multiplier = simpledialog.askfloat("Input", "Facteur de mult. (ex.: 0.5)")
    return _multiplier

# R_multiplier = 0