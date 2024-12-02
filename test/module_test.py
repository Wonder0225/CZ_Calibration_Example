# coding: utf-8
import sys
import os
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules import hamiltonian
from modules.parameters import *
from modules.visualization import CalibrationPlot

# calculate CZ properties
n_process = 15
step_w2 = 30
step_wc = 2 * step_w2
w2_peak_range = [-20.0, 30.0]
wc_min_range = [150.0, 600.0]

if __name__ == "__main__":
    
    # test the function of Hamiltonian
    args = {
        "gate time": 60,
        "coupler frequency": wc,
        "qubit2 frequency": w2
    }
    
    H_test = hamiltonian.Hamiltonian_RWA(args)
    
    # print(H_test(1))
    
    # test visualization
    data_address_fid = r"data/Population of state 110-test.npy"
    data_address_cphase = r"data/Conditional phase of state 110-test.npy"
    Plotter = CalibrationPlot(step_w2, step_wc, w2_peak_range, wc_min_range, data_address_fid, data_address_cphase)
    
    fig, ax = plt.subplots(1, 2, figsize=[11, 6])
    Plotter.plot_fidelity(fig, ax[0])
    Plotter.plot_cphase(fig, ax[1])