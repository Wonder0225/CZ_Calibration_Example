# coding: utf-8
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules import hamiltonian
from modules.parameters import *
from modules import pulse_generator

if __name__ == "__main__":
    
    # test the function of Hamiltonian
    args = {
        "gate time": 60,
        "coupler frequency": wc,
        "qubit2 frequency": w2
    }
    
    H_test = hamiltonian.Hamiltonian_RWA(args)
    
    # print(H_test(1))
    
    # test pulse_generator
    