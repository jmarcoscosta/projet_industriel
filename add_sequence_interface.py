from sequences_manager import *
import tkinter as tk
from verification_caracteristics import *
sequences_list = []
calibs_list = []
root = tk.Tk()
canvas1 = tk.Canvas(root, width=800, height=600)
canvas1.pack()
canvas1.configure(background="light blue")
root.title("Ajouter nouvelle séquence")

# Labels for each input text box
sequence_file_name_label = tk.Label(root, text="Nom du fichier: ",background="light blue")
canvas1.create_window(100, 50, window=sequence_file_name_label)
#
# Start_label = tk.Label(root, text="Début :",background="light blue")
# canvas1.create_window(100, 120, window=Start_label)
#
# Step_label = tk.Label(root, text="Pas :",background="light blue")
# canvas1.create_window(150, 120, window=Step_label)
#
# End_label = tk.Label(root,text="Fin :",background="light blue")
# canvas1.create_window(200,120,window=End_label)
#
# Unit_label = tk.Label(root, text="Unité:",background="light blue")
# canvas1.create_window(250, 120, window=Unit_label)
#
# Frequency_label = tk.Label(root, text="   Fréquence :",background="light blue")
# canvas1.create_window(300, 120, window=Frequency_label)

# Input text boxes
sequence_file_name_input = tk.Entry(root)
canvas1.create_window(230, 50, window=sequence_file_name_input)
#
# Start_input = tk.Entry(root, width=7)
# canvas1.create_window(100, 140, window=Start_input)
#
# Step_input = tk.Entry(root,width=7)
# canvas1.create_window(150, 140, window=Step_input)
#
# End_input = tk.Entry(root,width=7)
# canvas1.create_window(200, 140, window=End_input)
#
# Unit_input = tk.Entry(root,width=7)
# canvas1.create_window(250, 140, window=Unit_input)
#
# Frequency_input = tk.Entry(root,width=7)
# canvas1.create_window(300, 140, window=Frequency_input)

#####################################################################################
# Widgets for 'single command' insertion

module_label = tk.Label(root, text="Valeur:",background="light blue")
canvas1.create_window(100, 350, window=module_label)

unit_label = tk.Label(root, text="Unité:",background="light blue")
canvas1.create_window(150, 350, window=unit_label)

frequence_label = tk.Label(root,text="Fréquence :",background="light blue")
canvas1.create_window(200,350,window=frequence_label)


module_input = tk.Entry(root, width=7)
canvas1.create_window(100, 370, window=module_input )

unit_input = tk.Entry(root,width=7)
canvas1.create_window(150, 370, window=unit_input)

frequence_input = tk.Entry(root,width=7)
canvas1.create_window(200, 370, window=frequence_input)

command_option = tk.StringVar(root)
command_option.set("----") # default value

def add_command():
    sequence_string = ""
    add_frequency = False
    if command_option.get() == SEQUENCE_OPTIONS_LIST[0]:
        sequence_string = "- VDC "

    elif command_option.get() == SEQUENCE_OPTIONS_LIST[1]:
        sequence_string = "- VAC "
        add_frequency = True

    elif command_option.get() == SEQUENCE_OPTIONS_LIST[2]:
        sequence_string = "- IDC "

    elif command_option.get() == SEQUENCE_OPTIONS_LIST[3]:
        sequence_string = "- IAC "
        add_frequency = True

    elif command_option.get() == SEQUENCE_OPTIONS_LIST[4]:
        sequence_string = "- R "

    sequence_string += module_input.get()+" "+unit_input.get()

    if add_frequency:
        sequence_string += " "+frequence_input.get()
    sequences_list.append(sequence_string)
    # label_text = sequences_list_box.cget("text") + sequence_string + "\n"
    # label_text = sequences_list_box.cget("text") + str(len(sequences_list)) +") "+ sequence_string + "\n"
    label_text = seq_txt.get(1.0,tk.END)+ str(len(sequences_list)) +") "+ sequence_string + "\n"
    # sequences_list_box.configure(text=label_text)
    seq_txt.delete(1.0,tk.END)
    # seq_txt.insert(tk.END,sequences_list_box.cget("text"))
    seq_txt.insert(tk.END,label_text)
    update_numbering(seq_txt)


add_command_button = tk.Button(text='Ajouter', command=add_command)
canvas1.create_window(290, 370, window=add_command_button)

# Sequence options widgets:
SEQUENCE_OPTIONS_LIST = [
    "DC Tension",
    "AC Tension",
    "DC Current",
    "AC Current",
    "Resistance"
]


Command_options_menu = tk.OptionMenu(root, command_option, SEQUENCE_OPTIONS_LIST[0],
                                      SEQUENCE_OPTIONS_LIST[1], SEQUENCE_OPTIONS_LIST[2],
                                      SEQUENCE_OPTIONS_LIST[3], SEQUENCE_OPTIONS_LIST[4])


Command_options_menu.pack()
canvas1.create_window(230, 310, window=Command_options_menu)
Command_option_label = tk.Label(root, text="Type de commande:",background="light blue")
canvas1.create_window(100, 310, window=Command_option_label )
canvas1.create_rectangle(30,290,330,400)


##########################################################################################################""



option = tk.StringVar(root)
option.set("----") # default value

Sequence_options_menu = tk.OptionMenu(root, option, SEQUENCE_OPTIONS_LIST[0],
                                      SEQUENCE_OPTIONS_LIST[1], SEQUENCE_OPTIONS_LIST[2],
                                      SEQUENCE_OPTIONS_LIST[3], SEQUENCE_OPTIONS_LIST[4])


# Sequence_options_menu.pack()
# canvas1.create_window(230, 85, window=Sequence_options_menu)
# Sequence_option_label = tk.Label(root, text="Type de séquence:",background="light blue")
# canvas1.create_window(100, 85, window=Sequence_option_label)

sequences_list_label = tk.Label(root, text="Sequences:",background="light blue")
canvas1.create_window(600, 320, window=sequences_list_label)

sequences_list_box = tk.Label(root,background="AntiqueWhite1",width=30,height=15)
canvas1.create_window(600, 450, window=sequences_list_box)

calibration_range_list_label = tk.Label(root, text="Calibres:",background="light blue")
canvas1.create_window(600, 20, window=calibration_range_list_label)

calibration_range_list_box = tk.Label(root,background="AntiqueWhite1",width=30,height=15)
# scroll_calib = tk.Scrollbar(root, orient='vertical', command=calibration_range_list_box.yview)
canvas1.create_window(600, 150, window=calibration_range_list_box )

# def add_sequence():
#     sequence_string = ""
#     add_frequency = False
#     if option.get() == SEQUENCE_OPTIONS_LIST[0]:
#         sequence_string = "VDC "
#
#     elif option.get() == SEQUENCE_OPTIONS_LIST[1]:
#         sequence_string = "VAC "
#         add_frequency = True
#
#     elif option.get() == SEQUENCE_OPTIONS_LIST[2]:
#         sequence_string = "IDC "
#
#     elif option.get() == SEQUENCE_OPTIONS_LIST[3]:
#         sequence_string = "IAC "
#         add_frequency = True
#
#     elif option.get() == SEQUENCE_OPTIONS_LIST[4]:
#         sequence_string = "R "
#     sequence_string += Start_input.get()+":"+Step_input.get()+":"+End_input.get()+" "+Unit_input.get()
#
#     if add_frequency:
#         sequence_string += " "+Frequency_input.get()
#     sequences_list.append(sequence_string)
#     # label_text = sequences_list_box.cget("text") + sequence_string + "\n"
#     label_text = sequences_list_box.cget("text") + str(len(sequences_list)) +") "+ sequence_string + "\n"
#     sequences_list_box.configure(text=label_text)

# buttons
# add_sequence_button = tk.Button(text='Ajouter', command=add_sequence)
# canvas1.create_window(380, 140, window=add_sequence_button)

def export_sequence():
    from tkinter import messagebox
    update_calibs_list()
    update_sequences_list()
    # s_lines = seq_txt.get(1.0,tk.END).split("\n")
    n_lines_seq,_  = count_non_empty_lines(seq_txt)
    n_lines_calib,__ = count_non_empty_lines(calib_txt)
    # n_lines_seq = sum(1 for e in s_lines if e)
    # n_lines_calib = sum(1 for e in c_lines if e)
    if n_lines_seq != n_lines_calib:
        message = "The number of lines in Calibres and Sequences must be the same\n"
        message += "Calibres: "+str(n_lines_calib)+"\n"
        message += "Sequences: "+str(n_lines_seq)+"\n"
        messagebox.showerror("ERROR", message)
        return 0
    file = open(sequence_file_name_input.get()+".txt", "w+")
    file.write("FONCTION-CALIBRE-APPAREIL-ETALON-ECART-EMT-INCERTITUDE-CONFORMITE\n")
    for s,c in zip(sequences_list,calibs_list):
        s_words = s.split()
        c_words = c.split()
        function = s_words[2]
        value = s_words[3]
        unit = s_words[4]
        calib = c_words[1]
        ecart = str(0-float(value))
        print(calib)
        if len(s_words) == 6:
            frequency = s_words[-1]
            function = function+"_"+frequency
        line = function+"    "+calib+"_"+unit+"    #"+"    "+value
        line = line + "    "+ecart+"  remplir    remplir   NOK"
        file.write(line+"\n")
    file.close()

export_button = tk.Button(text="Exporter", command=export_sequence)
canvas1.create_window(150,450,window=export_button)

#
# def delete_sequence_by_number():
#     label_text = sequences_list_box.cget("text")
#     lines = label_text.split("\n")
#     lines.pop(int(seq_line_to_delete_input.get())-1)
#     new_text = "\n".join(lines)
#     sequences_list_box.configure(text=new_text)
#     sequences_list.pop(int(seq_line_to_delete_input.get())-1)
#     update_numbering(seq_txt)
#
#
# def delete_calib_by_number():
#     label_text = calibration_range_list_box.cget("text")
#     lines = label_text.split("\n")
#     lines.pop(int(calib_line_to_delete_input.get())-1)
#     new_text = "\n".join(lines)
#     calibration_range_list_box.configure(text=new_text)
#     calibs_list.pop(int(calib_line_to_delete_input.get())-1)
#     update_numbering(calib_txt)


def add_calib():
    calib_string = calib_value_input.get() +" "+calib_unit_input.get()
    # print(calib_string)
    calibs_list.append(calib_string)
    # label_text = calibration_range_list_box.cget("text") + str(len(calibs_list)) +") "+ calib_string+ "\n"
    label_text = calib_txt.get(1.0,tk.END)+ str(len(calibs_list)) +") "+ calib_string
    # calibration_range_list_box.configure(text=label_text)
    calib_txt.delete(1.0,tk.END)
    # calib_txt.insert(tk.END,calibration_range_list_box.cget("text"))
    calib_txt.insert(1.0,label_text)
    # txt.insert(tk.END,str(len(calibs_list)) +") "+ calib_string+ "\n")
    update_numbering(calib_txt)
    update_calibs_list()
    update_sequences_list()


# delete_sequence_by_number_button = tk.Button(text="Supp. n-ème ligne (Seq.)", command=delete_sequence_by_number)
# canvas1.create_window(150,550,window=delete_sequence_by_number_button)
# seq_line_to_delete_input = tk.Entry(root)
# canvas1.create_window(300, 550, window=seq_line_to_delete_input )
#
# delete_calib_by_number_button = tk.Button(text="Supp. n-ème ligne (Calib.)", command=delete_calib_by_number)
# canvas1.create_window(150,500,window=delete_calib_by_number_button )
# calib_line_to_delete_input = tk.Entry(root)
# canvas1.create_window(300, 500, window=calib_line_to_delete_input)

def count_non_empty_lines(box):
    label_text = box.get(1.0,tk.END)
    raw_lines = label_text.split("\n")
    lines = []
    for l in raw_lines:
        if l:
            lines.append(l)
    # print("len",len(lines))
    return len(lines), lines


def update_numbering(box):
    # label_text = box.cget("text")
    # label_text = box.get(1.0,tk.END)
    # raw_lines = label_text.split("\n")
    # lines = []
    # for l in raw_lines:
    #     if l:
    #         lines.append(l)
    # print(lines)
    result = []
    # n_lines = len(filter('',lines))
    # n_lines = sum(1 for e in lines if e)
    n_lines, lines = count_non_empty_lines(box)
    # print("---")
    # print(n_lines)
    # print("---")
    if n_lines > 1:
        for n,l in enumerate(lines):
            line_parts = l.split(")")
            if not l.strip():
                # if n == 0:
                    # line_parts[0] =
                continue
            # print(line_parts)
            # if(n<n_lines):
            # print(n)
            line_parts[0] = str(n+1)
            result.append(')'.join(line_parts))
        box.delete(1.0,tk.END)
        box.insert(tk.END, "\n".join(result))




################################################
# calibration range widgets:

def get_unit_from_calib(string):
    splitted = string.split()
    unit = splitted[2]
    return unit

def get_value_from_calib(string):
    splitted = string.split()
    value = splitted[1]
    print("splitted =",splitted)
    return float(value)

def update_calibs_list():
    global calibs_list
    # calibs_list = []
    _, calibs_list = count_non_empty_lines(calib_txt)


def update_sequences_list():
    global sequences_list
    # sequences_list = []
    _, sequences_list = count_non_empty_lines(seq_txt)


def add_seq_from_list(list):
    for i in list:
        sequences_list.append(i)
        # label_text = sequences_list_box.cget("text") + str(len(sequences_list)) +") "+ i + "\n"
        label_text = seq_txt.get(1.0,tk.END) + str(len(sequences_list)) +") "+ i + "\n"
        # sequences_list_box.configure(text=label_text)
        seq_txt.delete(1.0,tk.END)
        seq_txt.insert(tk.END,label_text)
    update_numbering(seq_txt)
    # print(seq_txt.get(1.0,tk.END))


FUNCTION_OPTIONS_LIST = [
    "VDC Linéarité",
    "VDC Exactitude",
    "VAC Linéarité",
    "VAC Exactitude",
    "VAC Réponse en fréquence",
    "IDC Exactitude",
    "IAC Exactitude",
    "R Exactitude"
]

def add_single_calib(function,interval):
    point = int(interval)
    # print(len(calibs_list))
    value = get_value_from_calib(calibs_list[point - 1])
    unit = get_unit_from_calib(calibs_list[point - 1])
    seq_list = function(value, unit)
    add_seq_from_list(seq_list)

def add_multiple_calibs(function,interval):
    splitted = interval.split("-")
    first = int(splitted[0])
    last = int(splitted[1]) + 1
    values = []
    # unit = get_unit_from_calib(calibs_list[first - 1])
    units = []
    for i in range(first, last):
        # print(len(calibs_list))
        values.append(get_value_from_calib(calibs_list[i - 1]))
        units.append(get_unit_from_calib(calibs_list[i - 1]))
    seq_list = function(values, units)
    add_seq_from_list(seq_list)

def add_sequence_from_calib():
    interval = calib_interval_input.get()
    print("before",len(calibs_list))
    update_calibs_list()
    update_sequences_list()
    print("after",len(calibs_list))

    if function_option.get() == FUNCTION_OPTIONS_LIST[0]:
        if interval.split("-")[0] is interval:
            add_single_calib(VDC_lin,interval)
        else:
            splitted = interval.split("-")
            first = int(splitted[0])
            add_single_calib(VDC_lin,first)

    elif function_option.get() == FUNCTION_OPTIONS_LIST[1]:
        if interval.split("-")[0] is interval:
            add_single_calib(VDC_exact,interval)
        else:
            add_multiple_calibs(VDC_exact,interval)

    elif function_option.get() == FUNCTION_OPTIONS_LIST[2]:
        if interval.split("-")[0] is interval:
            add_single_calib(VAC_lin,interval)
        else:
            splitted = interval.split("-")
            first = int(splitted[0])
            add_single_calib(VAC_lin,first)

    elif function_option.get() == FUNCTION_OPTIONS_LIST[3]:
        if interval.split("-")[0] is interval:
            add_single_calib(VAC_exact,interval)
        else:
            add_multiple_calibs(VAC_exact,interval)

    elif function_option.get() == FUNCTION_OPTIONS_LIST[4]:
        if interval.split("-")[0] is interval:
            add_single_calib(VAC_freq,interval)
        else:
            splitted = interval.split("-")
            first = int(splitted[0])
            add_single_calib(VAC_freq,first)
    elif function_option.get() == FUNCTION_OPTIONS_LIST[5]:
        if interval.split("-")[0] is interval:
            add_single_calib(IDC_exact,interval)
        else:
            add_multiple_calibs(IDC_exact,interval)

    elif function_option.get() == FUNCTION_OPTIONS_LIST[6]:
        if interval.split("-")[0] is interval:
            add_single_calib(IAC_exact,interval)
        else:
            add_multiple_calibs(IAC_exact,interval)

    elif function_option.get() == FUNCTION_OPTIONS_LIST[7]:

        # print(multiplier)
        if interval.split("-")[0] is interval:
            add_single_calib(R_exact,interval)
        else:
            add_multiple_calibs(R_exact,interval)
    update_calibs_list()
    update_sequences_list()
    # seq_txt.delete(1.0, tk.END)
    # seq_txt.insert(tk.END, sequences_list_box.cget("text"))



function_option = tk.StringVar(root)
function_option.set("----") # default value

Function_option_menu = tk.OptionMenu(root, function_option, FUNCTION_OPTIONS_LIST[0],
                                      FUNCTION_OPTIONS_LIST[1], FUNCTION_OPTIONS_LIST[2],
                                      FUNCTION_OPTIONS_LIST[3], FUNCTION_OPTIONS_LIST[4],
                                      FUNCTION_OPTIONS_LIST[5], FUNCTION_OPTIONS_LIST[6],
                                      FUNCTION_OPTIONS_LIST[7])


Function_option_menu.pack()
canvas1.create_window(280, 220, window=Function_option_menu)


calib_value_label = tk.Label(root, text="Valeur:",background="light blue")
canvas1.create_window(100, 125, window=calib_value_label)

calib_unit_label = tk.Label(root, text="Unité:",background="light blue")
canvas1.create_window(150, 125, window=calib_unit_label)

calib_type_label = tk.Label(root,text="Fonction/Caractéristique du calibre:",background="light blue")
canvas1.create_window(140,220,window=calib_type_label)
calib_interval_input = tk.Entry(root,width=7)
canvas1.create_window(240,255,window=calib_interval_input)
interval_label = tk.Label(root,text="Intervalle de points de Calibre:", background="light blue")
canvas1.create_window(120,255,window=interval_label)
add_points_seq = tk.Button(text="Ajouter",command = add_sequence_from_calib)
canvas1.create_window(300,255,window=add_points_seq)

calib_value_input= tk.Entry(root, width=7)
canvas1.create_window(100, 150, window=calib_value_input)

calib_unit_input= tk.Entry(root,width=7)
canvas1.create_window(150, 150, window=calib_unit_input)

add_calib_button = tk.Button(text='Ajouter calibre', command=add_calib)
canvas1.create_window(250, 150, window=add_calib_button )
canvas1.create_rectangle(30,100,330,180)

canvas1.create_rectangle(30,200,330,280)

# from tkinter import ttk
# myentry = ttk.Entry(root, textvariable="aaaaaa", state='readonly')
# myscroll = ttk.Scrollbar(root, orient='horizontal', command=myentry.xview)
# canvas1.create_window(400,400,window=myentry)
import tkinter.scrolledtext as scrolledtext
calib_txt = scrolledtext.ScrolledText(root, undo=True,width=23,height=13)
canvas1.create_window(600,150,window=calib_txt )

seq_txt = scrolledtext.ScrolledText(root, undo=True,width=23,height=13)
canvas1.create_window(600,450,window=seq_txt)


################################################

root.mainloop()

#################################################
