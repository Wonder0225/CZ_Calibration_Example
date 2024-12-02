# coding: utf-8
'''Run multiprocessing simulation for CZ calibration'''
import numpy as np
from modules.hamiltonian import Hamiltonian_RWA
from modules.gate_property import fidelity, cphase
from modules.parameters import *
import time
import multiprocessing
import os

class Calibration():
    
    def __init__(self, step_w2: int, step_wc: int, w2_peak_range: list[float], wc_min_range: list[float], n_process: int) -> None:
        '''
            Basic simulation parameeters
        '''
        
        self.step_w2 = step_w2
        self.step_wc = step_wc
        self.w2_peak_array = np.linspace(w2_peak_range[0], w2_peak_range[1], step_w2) * 1e-3 * 2 * np.pi + w1 + eta1
        self.wc_min_array = np.linspace(wc_min_range[0], wc_min_range[1], step_wc) * 1e-3 * 2 * np.pi + w1
        self.n_process = n_process
        
        pass
    
    def compute(self, target, wc_start, wc_end, w2_start, w2_end, idx, queue):
        '''
            Simulation tast for each process\\
            target = 1(fidelity), 2(phase)    
        '''
        
        count = 1
        data_list = []
        
        for wc_min in self.wc_min_array[wc_start:wc_end]:
            for w2_peak in self.w2_peak_array[w2_start:w2_end]: 

                args = {
                'coupler frequency': wc_min,
                'qubit2 frequency': w2_peak,
                'gate time': 60
            }

                H = Hamiltonian_RWA(args)

                if target == 1:
                    data_list.append(fidelity(H))
                elif target == 2:
                    data_list.append(cphase(H))
                else:
                    print("No such target!")
                    assert False
            
                print(f"Pool index: {idx}, count left = {(wc_end-wc_start)*(w2_end-w2_start) - count}")

                count += 1

        data_array = np.array(data_list)

        queue.put(data_array)

        pass
    
    def process_divide(self, target: int):
        '''target = 1(fidelity) / 2(cphase)'''
        
        t0 = time.time() # time count

        p_list = []
        queue_list = []
        step_part = int(self.step_w2/self.n_process)
        
        if int(step_part) != step_part:
            print("Error: step for each process is not an integer")
            assert int(step_part) == step_part
        
        for i in range(self.n_process):
            queue_list.append(multiprocessing.Manager().Queue())

        for i in range(self.n_process):
            p_list.append(multiprocessing.Process(target=self.compute, args=(target, step_part*i*int(self.step_wc/self.step_w2), step_part*(i+1)*int(self.step_wc/self.step_w2), 0, self.step_w2, i, queue_list[i], )))

        for p in p_list:
            p.start()

        for p in p_list:
            p.join()
        
        print(f"Done! Time cost: {time.time()-t0}s")
        
        return queue_list
    
    def calibrate(self, target: int, version: str):
        '''Start the calibration'''
        
        queue_list = self.process_divide(target)
        data_array = np.zeros(1)
        
        for i in range(self.n_process):
            data_array = np.append(data_array, queue_list[i].get())
            
        data_array = data_array[1:]
        
        if not os.path.exists('data'):
            os.makedirs('data')
        
        if target == 1:
            filename = rf"CZ_Calibration_Sample/data/Population of state 110-{str(version)}.npy"
        elif target == 2:
            filename = rf"CZ_Calibration_Sample/data/Conditional phase of state 110-{str(version)}.npy"
        else:
            print("Error: target not found!")
            assert False

        np.save(filename, data_array)

        pass