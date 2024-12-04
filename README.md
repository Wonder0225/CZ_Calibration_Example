# Control-Z gate qutip simulation
This is a simple but real example for superconducting circuit CZ gate calibration. Key parameters like waveform and qubit frequency are based on:  

- Sung, Y., Ding, L., Braumüller, J., Vepsäläinen, A., Kannan, B., Kjaergaard, M., Greene, A., Samach, G. O., McNally, C., Kim, D., Melville, A., Niedzielski, B. M., Schwartz, M. E., Yoder, J. L., Orlando, T. P., Gustavsson, S., & Oliver, W. D. (2021). Realization of High-Fidelity CZ and $ZZ$-Free iSWAP Gates with a Tunable Coupler. Physical Review X, 11(2), 021058. https://doi.org/10.1103/PhysRevX.11.021058

This program has following functions:
1. Solve the evolution of three qutrit system (q1-coupler-q2) in given qubit and coupler frequency.
2. Calibrate optimal control point for control-Z gate.
3. Execute quantum process tomography and visualize $\chi$ matrix.
4. *working on it...*

*To be mentioned, all the basic calculation procedures are done by **QuTip**.*
