import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import matplotlib.pyplot as plt
from modules.tomography import ProcessTomography
from modules.hamiltonian import Hamiltonian_RWA
import numpy as np
from qutip import mesolve
from modules.qutrit_operators import rho_110, psi_110

if __name__ == "__main__":
    
    qpt = ProcessTomography(r"CZ_Calibration_Example\data\optimal data\optimal parameters (wc, w2)-2.0.npy")
    
    fig = plt.figure()
    
    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    ax2 = fig.add_subplot(1, 2, 2, projection="3d")
    qpt.tomography2(fig, ax1, ax2)
    
    # optimal_point = np.load(r"CZ_Calibration_Example\data\optimal data\optimal parameters (wc, w2)-2.0.npy")
    # args = {
    #     'gate time': 60,
    #     'coupler frequency': optimal_point[0],
    #     'qubit2 frequency': optimal_point[1]
    # }
    # H = Hamiltonian_RWA(args)
    # result = mesolve(H, psi_110, np.linspace(0, 60, 100), [], [rho_110])
    # print(result.expect[0][-1])
    
    plt.show()