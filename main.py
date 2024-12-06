# coding: utf-8
import matplotlib.pyplot as plt
from modules.calibration import Calibration
from modules.visualization import CalibrationPlot
from modules.tomography import *
from modules.fine_tuning import FineTuning

if __name__ == "__main__":
    
    version = "3.1"
    
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

    # # quantum process tomography
    # fig = plt.figure(figsize=[11, 6]) # type: ignore
    # ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    # ax2 = fig.add_subplot(1, 2, 2, projection="3d")
    # qpt = ProcessTomography(optimal_data_save+rf"\optimal parameters (wc, w2)-{version}.npy")
    # chi_ideal, chi_exper = qpt.tomography2(fig, ax1, ax2)
    # print("Gate fidelity: "+tomo_fidelity(chi_ideal, chi_exper))
    # fig.savefig(rf"CZ_Calibration_Example\image\qpt\Quantum prosess tomography-{version}.png")
    
    # parameter fine tuning
    n_repeat_max_wc = 50
    n_repeat_max_w2 = 20
    n_process = 10
    step_wc = 50
    step_w2 = 20
    step_range_wc = 60 * 2 * np.pi * 1e-3 # MHz
    step_range_w2 = 5 * 2 * np.pi * 1e-3 # MHz
    
    ft_wc = FineTuning(optimal_data_save+rf"\optimal parameters (wc, w2)-3.0.npy", n_repeat_max_wc, n_process, step_wc=step_wc, step_range_wc=step_range_wc)
    ft_w2 = FineTuning(optimal_data_save+rf"\optimal parameters (wc, w2)-3.0.npy", n_repeat_max_w2, n_process, step_w2=step_w2, step_range_w2=step_range_w2)
    ft_wc.finetuning(1, version)
    ft_w2.finetuning(2, version)