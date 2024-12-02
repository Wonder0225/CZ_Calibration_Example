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
        
        if data_address_fid != None:
            self.data_fid = np.load(data_address_fid).reshape((step_wc, step_w2))
        
        if data_address_cphase != None:
            self.data_cphase = np.load(data_address_cphase).reshape((step_wc, step_w2))
        
        # directly calculate the optimal point by multiply the matrix
        self.if_optimal = False
        if data_address_cphase!= None and data_address_cphase != None:
            self.if_optimal = True
            data = abs(self.data_fid*self.data_cphase)
            optimal_idx = np.argmax(data)
            self.optimal_idx = [int(np.floor(optimal_idx/step_w2)), int(optimal_idx-np.floor(optimal_idx/step_w2)*step_w2)]
        
        pass
        
    def plot_fidelity(self, fig, ax):
        '''Plot fidelity distribution for state |110>'''
        
        ax0 = ax.matshow(self.data_fid, cmap="grey")
        fig.colorbar(ax0, ax=ax)
        ax.set_xticks(np.linspace(0, self.step_w2-1, 6), [f"{n:.3}" for n in self.f2_peak_array[np.linspace(0, self.step_w2-1, 6, dtype=int)]])
        ax.set_yticks(np.linspace(0, self.step_wc-1, 6), [f"{n:.3}" for n in self.fc_min_array[np.linspace(0, self.step_wc-1, 6, dtype=int)]])
        ax.set_xlabel(r"$f_2^{\text{peak}}-(f_1+\eta_1/2\pi)$ / MHz")
        ax.set_ylabel(r"$f_c^{\text{min}} - f_1$ / MHz")
        ax.set_title(r"Population of $|110\rangle$")
        
        if self.if_optimal == True:
            ax.plot(self.optimal_idx[1], self.optimal_idx[0], 'r.')
        
        pass
    
    def plot_cphase(self, fig, ax):
        '''Plot the conditional phase calculated by a cross-Ramsey type experiment'''
        
        ax1 = ax.matshow(self.data_cphase, cmap="twilight")
        fig.colorbar(ax1, ax=ax)
        ax.set_xticks(np.linspace(0, self.step_w2-1, 6), [f"{n:.3}" for n in self.f2_peak_array[np.linspace(0, self.step_w2-1, 6, dtype=int)]])
        ax.set_yticks(np.linspace(0, self.step_wc-1, 6), [f"{n:.3}" for n in self.fc_min_array[np.linspace(0, self.step_wc-1, 6, dtype=int)]])
        ax.set_xlabel(r"$f_2^{\text{peak}}-(f_1+\eta_1/2\pi)$ / MHz")
        ax.set_ylabel(r"$f_c^{\text{min}} - f_1$ / MHz")
        ax.set_title(r"Conditional phase of $|110\rangle$")
        
        if self.if_optimal == True:
            ax.plot(self.optimal_idx[1], self.optimal_idx[0], 'r.')

        pass