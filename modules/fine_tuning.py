# coding: utf-8
import numpy as np
from modules.calibration import Calibration
from modules.hamiltonian import Hamiltonian_RWA
from modules.gate_property import fidelity, cphase
import time
import multiprocessing
import os

class FineTuning(Calibration):
    '''Repeat CZ pusle several times for fine tuning'''

    def __init__(self, optimal_data_save: str, n_repeat_max: int, n_process: int, step_wc: int = 0, step_w2: int = 0, step_range_wc: float = 0, step_range_w2: float = 0):
        '''Input fine calibration range and repeat the gate '''
        
        # load optimal parameters
        data = np.load(optimal_data_save)
        self.wc_min = data[0]
        self.w2_peak = data[1]
        w2_peak_range = [self.w2_peak-step_range_w2, self.w2_peak+step_range_w2]
        wc_min_range = [self.wc_min-step_range_wc, self.wc_min+step_range_wc]
        
        super().__init__(step_w2, step_wc, w2_peak_range, wc_min_range, n_process)

        self.n_repeat_max = n_repeat_max

        pass
    
    def compute(self, target: int, w_start: float, w_end: float, process_idx: int, queue): # type: ignore
        '''
            Run fine tuning process
            target = 1(fidelity), 2(phase)
        '''

        count = 1
        data_list = []
        
        if target == 1:
            w_array = self.wc_min_array[w_start:w_end]
        elif target == 2:
            w_array = self.w2_peak_array[w_start:w_end]
        else:
            print("Error: tuning target not found!")
            assert target == 1 or target == 2
            
        print(f"process: {process_idx} start fine tuning.")
        
        for w in w_array: # type: ignore
            for n in range(self.n_repeat_max):
                n += 1
                args = {
                    'gate time': 60,
                    'coupler frequency': w if target == 1 else self.wc_min,
                    'qubit2 frequency': w if target == 2 else self.w2_peak,
                    'if_tuning': True,
                    'repeat time': n
                }
                
                H = Hamiltonian_RWA(args)
                
                data_list.append(fidelity(H)) if target == 1 else data_list.append(cphase(H))
                
                print(f"Pool index: {process_idx}, count left: {int(self.n_repeat_max*(w_end-w_start))-count}")
                
                count += 1
                
        data_array = np.array(data_list)
        
        queue.put(data_array)
        
        pass
    
    def process_divide(self, target): # type: ignore
        '''target = 1(fidelity) / 2(cphase)'''
        
        t0 = time.time()
        
        p_list = []
        queue_list = []
        step_part = int(self.step_wc/self.n_process) if target == 1 else int(self.step_w2/self.n_process)
        
        if int(step_part) != step_part:
            print("Error: step for each process is not an integer")
            assert int(step_part) == step_part
            
        for i in range(self.n_process):
            queue_list.append(multiprocessing.Manager().Queue())
            
        for i in range(self.n_process):
            p_list.append(multiprocessing.Process(target=self.compute, args=(target, step_part*i, step_part*(i+1), i, queue_list[i], )))
        
        for p in p_list:
            p.start()
            
        for p in p_list:
            p.join()            
        
        print(f"Done! Time cost: {time.time()-t0}s")
        
        return queue_list
    
    def finetuning(self, target: int, version: str):
        '''Start finetuning'''
        
        queue_list = self.process_divide(target)
        data_array = np.zeros(1)
        
        for i in range(self.n_process):
            data_array = np.append(data_array, queue_list[i].get())
            
        data_array = data_array[1:]
        
        if not os.path.exists('data/finetuning'):
            os.makedirs('data/finetuning')
            
        if target == 1:
            filename = rf"CZ_Calibration_Example/data/finetuning/Finetuning for coupler frequency-{version}.npy"
        elif target == 2:
            filename = rf"CZ_Calibration_Example/data/finetuning/Finetuning for qubit2 frequency-{version}.npy"
        else:
            print("Error: target not found!")
            assert False
            
        np.save(filename, data_array)
        
        pass