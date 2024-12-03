# coding: utf-8
'''
    creation and annihilation perators for qutrits\\
    density matrix for targeted states
'''
from qutip import tensor, qeye, destroy, basis, ket2dm # type: ignore

# operators of three qutrit (Q1, Q2, CPLR)
b1 = tensor(destroy(3), qeye(3), qeye(3))
b1dag = b1.dag()
b2 = tensor(qeye(3), destroy(3), qeye(3))
b2dag = b2.dag()
bc = tensor(qeye(3), qeye(3), destroy(3))
bcdag = bc.dag()

# density matrix for targeted states
psi_000 = tensor(basis(3, 0), basis(3, 0), basis(3, 0))
psi_010 = tensor(basis(3, 0), basis(3, 1), basis(3, 0))
psi_100 = tensor(basis(3, 1), basis(3, 0), basis(3, 0))
psi_110 = tensor(basis(3, 1), basis(3, 1), basis(3, 0))
rho_010 = ket2dm(tensor(basis(3, 0), basis(3, 1), basis(3, 0)))
rho_100 = ket2dm(tensor(basis(3, 1), basis(3, 0), basis(3, 0)))
rho_110 = ket2dm(tensor(basis(3, 1), basis(3, 1), basis(3, 0)))
rho_200 = ket2dm(tensor(basis(3, 2), basis(3, 0), basis(3, 0))) # leakage state
rho_p00 = ket2dm(tensor((basis(3, 0)+basis(3, 1)).unit(), basis(3, 0), basis(3, 0))) # Ramsey-type experiment
rho_p10 = ket2dm(tensor((basis(3, 0)+basis(3, 1)).unit(), basis(3, 1), basis(3, 0))) # Ramsey-type experiment

# two energy level states for qpt
psi_00 = tensor(basis(2, 0), basis(2, 0))
psi_01 = tensor(basis(2, 0), basis(2, 1))
psi_10 = tensor(basis(2, 1), basis(2, 0))
psi_11 = tensor(basis(2, 1), basis(2, 1))