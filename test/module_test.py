# coding: utf-8
import sys
import os
import time
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules import hamiltonian
from modules.parameters import *
from modules.visualization import CalibrationPlot, plot_waveform
from modules.gate_property import cphase, fidelity

# calculate CZ properties
n_process = 15
step_w2 = 60
step_wc = 2 * step_w2
w2_peak_range = [-20.0, 30.0]
wc_min_range = [150.0, 600.0]

if __name__ == "__main__":

    data_optimal = np.load(r"CZ_Calibration_Example\data\optimal data\optimal parameters (wc, w2)-2.0.npy")
    print(data_optimal)
    
    # test the function of Hamiltonian
    args = {
        "gate time": 60,
        "coupler frequency": data_optimal[0],
        "qubit2 frequency": data_optimal[1],
        "if_tuning": True,
        "repeat time": 10
    }
    
    H_test = hamiltonian.Hamiltonian_RWA(args)
    
    # print(H_test(1))
    
    # test visualization
    # data_address_fid = r"CZ_Calibration_Example/test/data/Population of state 110-1.0.npy"
    # data_address_cphase = r"CZ_Calibration_Example/test/data/Conditional phase of state 110-1.0.npy"
    # optimal_data_save = r"CZ_Calibration_Example/test/data"
    # Plotter = CalibrationPlot(step_w2, step_wc, w2_peak_range, wc_min_range, data_address_fid, data_address_cphase)
    
    # fig, ax = plt.subplots(1, 2, figsize=[11, 6])
    # Plotter.plot_fidelity(fig, ax[0])
    # Plotter.plot_cphase(fig, ax[1])
    # Plotter.save_optimal(optimal_data_save, "1.0")

    fig, ax = plt.subplots(1, 1)
    plot_waveform(args, ax)
    plt.show()
    
    # test cphase calculation
    # cphase(H_test)