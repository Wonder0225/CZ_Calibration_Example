# coding: utf-8
import numpy as np
from qutip import QobjEvo # type: ignore
from modules.pulse_generator import *

w_2 = Pulse_Qubit2
w_c = Pulse_Coupler
g_1c = CouplingStrength_1c
g_2c = CouplingStrength_2c
g_12 = CouplingStrength_12

def Hamiltonian_RWA(args: dict):
    '''Construct system Hamiltonian (RWA)'''

    H_nl = 0.5 * (eta1 * b1dag**2 * b1**2 + eta2 * b2dag**2 * b2**2 + etac * bcdag**2 * bc**2)
    H_l1 = w1 * b1dag * b1
    H_l2 = [b2dag * b2, w_2]
    H_lc = [bcdag * bc, w_c]
    H_q1c = [- b1 * bcdag - b1dag * bc, g_1c]
    H_q2c = [- b2 * bcdag - b2dag * bc, g_2c]
    H_q12 = [- b1 * b2dag - b1dag * b2, g_12]

    return QobjEvo([H_nl, H_l1, H_l2, H_lc, H_q1c, H_q2c, H_q12], args=args) # type: ignore