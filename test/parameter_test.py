import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.qutrit_operators import rho_110
from qutip import gates

if __name__ == "__main__":
    
    print(rho_110 * rho_110.dag())
    print(gates.cz_gate())