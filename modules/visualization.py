# coding: utf-8
import numpy as np
from modules.calibration import Calibration
from modules.fine_tuning import FineTuning
import os
from modules.pulse_generator import Pulse_Coupler, Pulse_Qubit2
from modules.parameters import *

def plot_waveform(args: dict, ax):
    '''Visualize the waveform used in simulation'''

    if args['if_tuning'] == False:
        tlist = np.linspace(0, 60, 100)
    else:
        tlist = np.linspace(0, 60*args['repeat time'], 100*args['repeat time'])

    ax.plot(tlist, Pulse_Coupler(tlist, args)) # type: ignore
    ax.plot(tlist, Pulse_Qubit2(tlist, args)) # type: ignore
    ax.plot(tlist, w1*np.ones(len(tlist)))

    pass

class CalibrationPlot(Calibration):
    '''Plot figures for CZ gate calibration'''
    
    def __init__(self, step_w2: int, step_wc: int, w2_peak_range: list[float], wc_min_range: list[float], data_address_fid: str = None, data_address_cphase: str = None): # type: ignore
        '''Input Basic parameters for CZ calibration.'''
        
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
    
    def save_optimal(self, optimal_data_save: str, version: str):
        '''Save the optimal point'''
        
        save_address = optimal_data_save + rf"\optimal parameters (wc, w2)-{version}.npy"
        
        if not os.path.exists('data'):
            os.makedirs('data')
            
        if self.if_optimal == False:
            print("Error: not enough data for calculating optimal point!")
            assert self.if_optimal
            
        np.save(save_address, np.array([self.wc_min_array[self.optimal_idx[0]], self.w2_peak_array[self.optimal_idx[1]]]))
            
        pass
    
class TuningPlot(FineTuning):
    '''Visualize fine tuning consequence'''
    
    def __init__(self, optimal_data_save: str, step_wc: int = 0, step_w2: int = 0, step_range_wc: float = 0, step_range_w2: float = 0, data_fine_wc: str = None, data_fine_w2: str = None): # type: ignore
        '''Input basic parameters for CZ fine tuning.'''
        
        super().__init__(optimal_data_save, None, None, step_wc, step_w2, step_range_wc, step_range_w2) # type: ignore
        
        self.f2_peak_array = self.w2_peak_array / 2 / np.pi
        self.fc_min_array = self.wc_min_array / 2 / np.pi
        
        if data_fine_wc != None:
            data_wc = np.load(data_fine_wc)
            self.n_repeat_max = int(len(data_wc)/step_wc)
            self.data_wc = data_wc.reshape((step_wc, int(len(data_wc)/step_wc)))
        
        if data_fine_w2 != None:
            data_w2 = np.load(data_fine_w2)
            self.n_repeat_max = int(len(data_w2)/step_w2)
            self.data_w2 = data_w2.reshape((step_w2, int(len(data_w2)/step_w2)))
            
    def plot_wc_ft(self, fig, ax):
        '''Plot wc fine tuning consequence'''
        
        ax0 = ax.matshow(self.data_wc, cmap="grey")
        fig.colorbar(ax0, ax=ax)
        ax.set_yticks(np.linspace(0, self.step_wc-1, 6), [f"{n:.3}" for n in self.fc_min_array[np.linspace(0, self.step_wc-1, 6, dtype=int)]])
        ax.set_xlabel(r"$n_{\text{CZ}}$")
        ax.set_ylabel(r"$f_c^{\text{min}} - f_1$ / MHz")
        ax.set_title(r"$f_c$ fine tuning")
        
        pass
    
    def plot_w2_ft(self, fig, ax):
        '''Plot the conditional phase calculated by a cross-Ramsey type experiment'''
        
        ax1 = ax.matshow(self.data_w2, cmap="twilight")
        fig.colorbar(ax1, ax=ax)
        ax.set_yticks(np.linspace(0, self.step_w2-1, 6), [f"{n:.3}" for n in self.f2_peak_array[np.linspace(0, self.step_w2-1, 6, dtype=int)]])
        ax.set_xlabel(r"$n_{\text{CZ}}$")
        ax.set_ylabel(r"$f_2^{\text{peak}}-(f_1+\eta_1/2\pi)$ / MHz")
        ax.set_title(r"Conditional phase of $|110\rangle$")

        pass