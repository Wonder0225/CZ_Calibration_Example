# coding: utf-8
from qutip import Qobj, mesolve, ket2dm
import numpy as np
from modules.qutrit_operators import rho_110, rho_p00, rho_p10

def fidelity(H: Qobj, tg: float = 60) -> float:
    '''Calculate CZ gate fidelity.'''
    
    tlist = np.linspace(0, tg, int(tg+5))
    result = mesolve(H, rho_110, tlist, [], [rho_110])
    
    return result.expect[0][-1]

def phase(c0: complex, c1: complex) -> float:
    '''Calculate the phase difference between two complex number'''

    c0_unit = c0 / abs(c0)
    c1_unit = c1 / abs(c1)
    z = c1_unit / c0_unit

    if np.real(z) < 0:
        if np.imag(z) < 0:
            return np.arccos(np.real(z))
        else:
            return -np.arccos(np.real(z))
    else:
        return -np.arcsin(np.imag(z))

def cphase(H: Qobj, tg: float = 60) -> float:
    '''Calculate conditional phase with Ramsey-type experiment'''
    
    tlist = np.linspace(0, tg, int(tg+5))
    result_p00 = mesolve(H, rho_p00, tlist, [], [])
    result_p10 = mesolve(H, rho_p10, tlist, [], [])
    
    rho2_p00_final = result_p00.states[-1].ptrace(1)
    rho2_p10_final = result_p10.states[-1].ptrace(1)
    
    return phase(rho2_p00_final[0, 1], rho2_p10_final[0, 1])