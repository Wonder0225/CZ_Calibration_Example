import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import matplotlib.pyplot as plt
from modules.tomography import ProcessTomography, tomo_fidelity
from qutip import about

if __name__ == "__main__":
    
    qpt = ProcessTomography(r"CZ_Calibration_Example\data\optimal data\optimal parameters (wc, w2)-2.0.npy")
    
    fig = plt.figure()
    
    ax1 = fig.add_subplot(1, 2, 1, projection="3d")    
    ax2 = fig.add_subplot(1, 2, 2, projection="3d")
    [chi_ideal, chi_real] = qpt.tomography2(fig, ax1, ax2)
    
    print(tomo_fidelity(chi_ideal, chi_real)*4)
    print(chi_real.trace())
    print(chi_ideal.trace())
    
    # plt.show()
    print(about())