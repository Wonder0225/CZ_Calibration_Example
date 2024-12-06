# coding: utf-8
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.visualization import TuningPlot
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    
    optimal_data_save = rf"CZ_Calibration_Example\data\optimal data"
    
    n_repeat_max_wc = 50
    n_repeat_max_w2 = 20
    n_process = 10
    step_wc = 50
    step_w2 = 20
    step_range_wc = 60 * 2 * np.pi * 1e-3 # MHz
    step_range_w2 = 5 * 2 * np.pi * 1e-3 # MHz
    
    data_fine_wc = r"CZ_Calibration_Example\data\finetuning\Finetuning for coupler frequency-3.1.npy"
    data_fine_w2 = r"CZ_Calibration_Example\data\finetuning\Finetuning for qubit2 frequency-3.1.npy"
    
    tp = TuningPlot(optimal_data_save+rf"\optimal parameters (wc, w2)-3.0.npy", step_wc, step_w2, step_range_wc, step_range_w2, data_fine_wc, data_fine_w2)
    
    fig, ax = plt.subplots(1, 2)
    tp.plot_wc_ft(fig, ax[0])
    tp.plot_w2_ft(fig, ax[1])
    
    plt.show()