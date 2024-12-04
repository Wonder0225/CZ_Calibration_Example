# coding: utf-8
import matplotlib.pyplot as plt
from modules.calibration import Calibration
from modules.visualization import CalibrationPlot
from modules.tomography import *

if __name__ == "__main__":
    
    version = "2.0"
    
    # # calculate CZ properties
    # n_process = 12
    # step_w2 = 60
    # step_wc = 2 * step_w2
    # w2_peak_range = [-20.0, 30.0]
    # wc_min_range = [150.0, 450.0]
    
    # Simulate = Calibration(step_w2, step_wc, w2_peak_range, wc_min_range, n_process)
    
    # Simulate.calibrate(1, version)
    # Simulate.calibrate(2, version)
    
    # # visualization the consequence
    # data_address_fid = rf"CZ_Calibration_Example\data\Population of state 110-{version}.npy"
    # data_address_cphase = rf"CZ_Calibration_Example\data\Conditional phase of state 110-{version}.npy"
    optimal_data_save = rf"CZ_Calibration_Example\data\optimal data"
    
    # Plot = CalibrationPlot(step_w2, step_wc, w2_peak_range, wc_min_range, data_address_fid, data_address_cphase)
    
    # fig, ax = plt.subplots(1, 2, figsize=[11, 6])
    # Plot.plot_fidelity(fig, ax[0])
    # Plot.plot_cphase(fig, ax[1])
    # Plot.save_optimal(optimal_data_save, version)
    
    # fig.savefig(rf"CZ_Calibration_Example/image/calibration consequence-{version}.png")

    # quantum process tomography
    fig = plt.figure(figsize=[11, 6])
    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    ax2 = fig.add_subplot(1, 2, 2, projection="3d")
    qpt = ProcessTomography(optimal_data_save+rf"\optimal parameters (wc, w2)-{version}.npy")
    qpt.tomography2(fig, ax1, ax2)
    fig.savefig(rf"CZ_Calibration_Example\image\qpt\Quantum prosess tomography-{version}.png")