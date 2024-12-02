# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
from modules.calibration import Calibration

class CalibrationPlot(Calibration):
    '''Plot figures for CZ gate calibration'''
    
    def __init__(self, step_w2: int, step_wc: int, w2_peak_range: list[float], wc_min_range: list[float], data_address_fid: str = None, data_address_cphase: str = None, ): # type: ignore
        
        super().__init__(step_w2, step_wc, w2_peak_range, wc_min_range, None) # type:ignore
        
        self.f2_peak_array = self.w2_peak_array / 2 / np.pi
        self.fc_min_array = self.wc_min_array / 2 / np.pi
        self.data_address_fid = data_address_fid
        self.data_address_cphase = data_address_cphase
        
        pass
        
    def plot_fidelity(self, fig, ax):
        '''Plot fidelity distribution for state |110>'''
        
        data = np.load(self.data_address_fid).reshape((self.step_wc, self.step_w2))
        ax0 = ax.matshow(data, cmap="grey")
        fig.colorbar(ax0, ax=ax)
        ax.set_xticks(np.linspace(0, self.step_w2-1, 6), [f"{n:.3}" for n in self.f2_peak_array[np.linspace(0, self.step_w2-1, 6, dtype=int)]])
        ax.set_yticks(np.linspace(0, self.step_wc-1, 6), [f"{n:.3}" for n in self.fc_min_array[np.linspace(0, self.step_wc-1, 6, dtype=int)]])
        ax.set_xlabel(r"$f_2^{\text{peak}}-(f_1+\eta_1/2\pi)$ / MHz")
        ax.set_ylabel(r"$f_c^{\text{min}} - f_1$ / MHz")
        ax.set_title(r"Population of $|110\rangle$")
        
        pass
    
    def plot_cphase(self, fig, ax):
        
        data_cphase = np.load(self.data_address_cphase).reshape((self.step_wc, self.step_w2))
        ax1 = ax.matshow(data_cphase, cmap="twilight")
        fig.colorbar(ax1, ax=ax)
        ax.set_xticks(np.linspace(0, self.step_w2-1, 6), [f"{n:.3}" for n in self.f2_peak_array[np.linspace(0, self.step_w2-1, 6, dtype=int)]])
        ax.set_yticks(np.linspace(0, self.step_wc-1, 6), [f"{n:.3}" for n in self.fc_min_array[np.linspace(0, self.step_wc-1, 6, dtype=int)]])
        ax.set_xlabel(r"$f_2^{\text{peak}}-(f_1+\eta_1/2\pi)$ / MHz")
        ax.set_ylabel(r"$f_c^{\text{min}} - f_1$ / MHz")
        ax.set_title(r"Conditional phase of $|110\rangle$")

        pass
    
    def plot_optimal(self, ax_list: list):
        
        pass