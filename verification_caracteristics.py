# lin : linearite
# freq: réponse en fréquence
# exact: exactitude

from tkinter import messagebox
from tkinter import *

def VDC_lin(points, unit):
    result = []
    multipliers = [0.1,0.5,0.9,-0.9]
    for m in multipliers:
        result.append("- VDC "+str(points*m)+" "+unit.upper())
    return result


def VDC_exact(points, units):
    result = []
    try:
        iterator = iter(points)
    except TypeError:
        result.append("- VDC "+str(points*0.5)+" "+units.upper()) # single calib
    else:
        for p,u in zip(points,units):
            result.append("- VDC "+str(p*0.5)+" "+u.upper()) # multiple calibs
    return result

def VAC_lin(point, unit):
    result = []
    multipliers = [0.1, 0.5, 0.9]
    for m in multipliers:
        result.append("- VAC " + str(point* m) + " " + unit.upper()+" 50")
    return result

def VAC_exact(points, units):
    result = []
    try:
        iterator = iter(points)
    except TypeError:
        result.append("- VAC "+str(points*0.5)+" "+units.upper()+" 50")
    else:
        for p,u in zip(points,units):
            result.append("- VAC "+str(p*0.5)+" "+u.upper()+" 50")
    return result

def VAC_freq(point, unit):
    result = []
    freqs = [50, 400, 1000]
    for f in freqs:
        result.append("- VAC " + str(point * 0.5) + " " + unit.upper() + " "+str(f))
    return result

def IDC_exact(points, units):
    result = []
    try:
        iterator = iter(points)
    except TypeError:
        result.append("- IDC "+str(points*0.5)+" "+units.upper())
    else:
        for p, u in zip(points,units):
            result.append("- IDC "+str(p*0.5)+" "+u.upper())
    return result

def IAC_exact(points, units):
    result = []
    try:
        iterator = iter(points)
    except TypeError:
        result.append("- IAC "+str(points*0.5)+" "+units.upper()+" 50")
    else:
        for p, u in zip(points,units):
                result.append("- IAC "+str(p*0.5)+" "+u.upper()+" 50")
    return result


def R_exact(points, units):
    from sequences_manager import pop_up_R
    result = []
    try:
        iterator = iter(points)
    except TypeError:
        result.append("- R "+str(points*pop_up_R())+" "+units.upper())
    else:
        multiplier = pop_up_R()
        for p, u in zip(points,units):
            result.append("- R "+str(p*multiplier)+" "+u.upper())
    return result



def R_mult(start,ratio,number_of_points):
    result = []
    for i in range(number_of_points):
        result.append("- R "+str(start*ratio**i))
    return result
