# coding: utf-8
import numpy as np
from scipy import special
from modules.parameters import *
from modules.qutrit_operators import *

# frequency pulse generator (a_b represents a function)
def Pulse_Coupler(t: float, args: dict) -> float:
    '''Input Z pulse for coupler'''

    wct = args['coupler frequency']
    tg = args['gate time']

    output = wc - (wc - wct) * (special.erf(t - np.e) - special.erf(t - tg + np.e)) * 0.5

    if args['if_tuning'] == True:
        n_repeat = args['repeat time']
        for i in range(n_repeat-1):
            output -= (wc - wct) * (special.erf(t-60*(i+1) - np.e) - special.erf(t-60*(i+1) - tg + np.e)) * 0.5

    return output

def Pulse_Qubit2(t: float, args: dict) -> float:
    '''Input Z pulse for qubit 2'''

    w2t = args['qubit2 frequency']
    tg = args['gate time']

    output = w2 - (w2 - w2t) * (special.erf(t - np.e) - special.erf(t - tg + np.e)) * 0.5

    if args['if_tuning'] == True:
        n_repeat = args['repeat time']
        for i in range(n_repeat-1):
            output -= (w2 - w2t) * (special.erf(t-60*(i+1) - np.e) - special.erf(t-60*(i+1) - tg + np.e)) * 0.5

    return output

# coupling strength
def CouplingStrength_1c(t: float, args: dict) -> float:
    '''Coupling strength between qubit 1 (fixed) and coupler (tunable)'''

    output = 0.5 * C1c / np.sqrt(C1 * Cc) * np.sqrt(w1 * Pulse_Coupler(t, args))

    return output

def CouplingStrength_2c(t: float, args: dict) -> float:
    '''Coupling strength between qubit 2 (tunable) and coupler (tunable)'''

    output = 0.5 * C2c / np.sqrt(C2 * Cc) * np.sqrt(Pulse_Qubit2(t, args) * Pulse_Coupler(t, args))

    return output

def CouplingStrength_12(t: float, args: dict) -> float:
    '''Coupling strength between qubit 1 (fixed) and qubit 2 (tunable)'''

    output = 0.5 * (C12 / np.sqrt(C1 * C2) + C1c * C2c / np.sqrt(C1 * C2 * Cc**2)) * np.sqrt(w1 * Pulse_Qubit2(t, args))

    return output