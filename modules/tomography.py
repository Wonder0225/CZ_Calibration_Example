# coding: utf-8
import numpy as np
from qutip import gates, to_super, qeye, sigmax, sigmay, sigmaz, tomography, mesolve, qzero, ket2dm
from modules.qutrit_operators import psi_000, psi_010, psi_100, psi_110, psi_10, psi_01, psi_00, psi_11
from modules.hamiltonian import Hamiltonian_RWA
from modules.gate_property import phase

class ProcessTomography():
    '''Run quantum process tomography (QPT)'''
    
    def __init__(self, optimal_data_save: str) -> None:
        '''Read the optimal data'''
        
        data = np.load(optimal_data_save)
        self.wc_min = data[0]
        self.w2_peak = data[1]
        
        args = {
            'gate time': 60,
            'coupler frequency': self.wc_min,
            'qubit2 frequency': self.w2_peak
        }
        self.H = Hamiltonian_RWA(args)
        
        pass
    
    def dphase(self):
        '''Calculate dynamic phase'''
        
        tlist = np.linspace(0, 60, 70)
        result_010 = mesolve(self.H, psi_010, tlist, [], [])
        result_100 = mesolve(self.H, psi_100, tlist, [], [])
        
        phi_q2 = phase(1, psi_010.dag()*result_010.states[-1])
        phi_q1 = phase(1, psi_100.dag()*result_100.states[-1])
        
        return phi_q1, phi_q2
        
    def tomography2(self, fig, ax1, ax2):
        '''QPT under Two Energy Level approximation'''
        
        basis = [[qeye(2), sigmax(), sigmay(), sigmaz()]] * 2
        label = [['i', 'x', 'y', 'z']] * 2
        
        Ucz_ideal = gates.cz_gate()
        Ucz_ideal_super = to_super(Ucz_ideal)
        chi_ideal = tomography.qpt(Ucz_ideal_super, basis)
        tomography.qpt_plot_combined(chi_ideal, label, fig=fig, ax=ax1, threshold=0.01)
        
        # dynamic phase correction
        [dphase_q1, dphase_q2] = self.dphase()
        Uphase_corr = qeye([2, 2]) + (np.exp(1j*dphase_q1)-1) * ket2dm(psi_10) + (np.exp(1j*dphase_q2)-1) * ket2dm(psi_01)
        
        # run qpt
        Ucz = qzero([2, 2])
        tlist = np.linspace(0, 60, 70)
        state_list = [psi_000, psi_010, psi_100, psi_110]
        psi_list = [psi_00, psi_01, psi_10, psi_11]
        for i in range(4):
            result_temp = mesolve(self.H, state_list[i], tlist, [], [ket2dm(state) for state in state_list])
            for j in range(4):
                Ucz += result_temp.expect[j][-1] * psi_list[j] * psi_list[i].dag()
                
        Ucz = Uphase_corr * Ucz
        print(Ucz)
        Ucz_super = to_super(Ucz)
        chi_simulate = tomography.qpt(Ucz_super, basis)
        tomography.qpt_plot_combined(chi_simulate, label, fig=fig, ax= ax2, threshold=0.01)
        
        return chi_ideal, chi_simulate