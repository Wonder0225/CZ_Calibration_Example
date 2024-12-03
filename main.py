# coding: utf-8
import matplotlib.pyplot as plt
from modules.calibration import Calibration
from modules.visualization import CalibrationPlot

if __name__ == "__main__":
    
    version = "1.0"
    
    # calculate CZ properties
    n_process = 10
    step_w2 = 20
    step_wc = 2 * step_w2
    w2_peak_range = [-20.0, 30.0]
    wc_min_range = [150.0, 600.0]
    
    Simulate = Calibration(step_w2, step_wc, w2_peak_range, wc_min_range, n_process)
    
    Simulate.calibrate(1, version)
    Simulate.calibrate(2, version)
    
    # visualization the consequence
    data_address_fid = rf"CZ_Calibration_Example\data\Population of state 110-{version}.npy"
    data_address_cphase = rf"CZ_Calibration_Example\data\Conditional phase of state 110-{version}.npy"
    
    Plot = CalibrationPlot(step_w2, step_wc, w2_peak_range, wc_min_range, data_address_fid, data_address_cphase)
    
    fig, ax = plt.subplots(1, 2, figsize=[11, 6])
    Plot.plot_fidelity(fig, ax[0])
    Plot.plot_cphase(fig, ax[1])
    
    fig.savefig(rf"CZ_Calibration_Example/image/calibration consequence-{version}.png")