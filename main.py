# coding: utf-8
from modules.calibration import Calibration

if __name__ == "__main__":
    
    # calculate CZ properties
    n_process = 15
    step_w2 = 30
    step_wc = 2 * step_w2
    w2_peak_range = [-20.0, 30.0]
    wc_min_range = [150.0, 160.0]
    
    Simulate = Calibration(step_w2, step_wc, w2_peak_range, wc_min_range, n_process)
    
    Simulate.calibrate(1, "test")
    Simulate.calibrate(2, "test")