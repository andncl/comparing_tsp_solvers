"""Module containing G class"""
import copy
import logging
import typing_extensions
from importlib import reload

import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit import IBMQ, Aer, execute
from qiskit.tools.visualization import plot_histogram
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import Unroller

from .tsp_solver_base import TspSolverBase

class Grover(TspSolverBase):
    """ 
    The SimulatedAnnealer class formulates and solves the traveling salesman
    problem with the classical simulated annealing algorithm
    """
    def __init__(self) -> None:
        super().__init__()

    
    ## define required logical functions

    def OR(qubit_1: int, qubit_2, k: int):
        """ 
        Function does the equivalent of a classical OR between qubit numbers 
        a and b and stores the result in qubit number k 
        
        Args:
            qubit_1 (int): Index of qubit 1
            qubit_2 (int): Index of qubit 2    
        """
        self.qc.x(q[qubit_1])
        self.qc.x(q[qubit_2])
        self.qc.ccx(q[qubit_1], q[qubit_2], q[k])
        self.qc.x(q[k])
        self.qc.x(q[qubit_1])
        self.qc.x(q[qubit_2])


    def are_not_equal(self, a_0: int, b_0: int, k: int):
        # enter node numbers here. For example, a is node 0, b is node 1 and c 
        # is node 2
        """
        Function outputs 1 if nodes a and b are not the same. Node numbering 
        starts from 0 as in the problem statement. k is the qubit number where 
        the output is XOR-ed. qubit numbering also starts from 0
        
        Args:
            a_0 (int): Node number
            b_0 (int): Node number
            k (int): 

        """
        self.qc.cx(q[2*a_0], q[2*b_0])
        self.qc.cx(q[(2*a_0) + 1], q[(2*b_0) + 1])
        OR(2*b_0, (2*b_0)+1, k)
        self.qc.cx(q[2*a_0], q[2*b_0])
        self.qc.cx(q[(2*a_0) + 1], q[(2*b_0) + 1])

    def is_not_3(self, a: int, k: int):
        """Enter method docstring here"""
        self.qc.ccx(q[2*a], q[(2*a)+1], q[k])
        self.qc.x(q[k])

    def initialize_oracle_part(self, n: int):
        """Enter method docstring here"""
        t = 4
        self.are_not_equal(0, 1, 6) # node a and b are not equal 
        self.are_not_equal(0, 2, 7)
        self.are_not_equal(1, 2, 8)
        self.is_not_3(0, 11)
        self.is_not_3(1, 12)
        self.is_not_3(2, 13)
        self.qc.mct(
            [q[6], q[7], q[8], q[11], q[12], q[13]],
            q[10],
            [q[9], q[14], q[15], q[16]]
            )
        # answer is stored in 10. please keep 9 a clean qubit, it's used as 
        # ancilla here 
        self.is_not_3(0, 11)
        self.is_not_3(1, 12)
        self.is_not_3(2, 13)
        self.are_not_equal(0, 1, 6) # node a and b are not equal 
        self.are_not_equal(0, 2, 7)
        self.are_not_equal(1, 2, 8)
        
        ## distance_black_box, needs to become user-defined in next version

        distances = {
            "32": 3,
            "31": 2,
            "30": 4,
            "21": 7,
            "20": 6,
            "10": 5,
        }

    def initialize_oracle_part(self):
        """Enter method docstring here"""
        qr = QuantumRegister(2)
        qr_target = QuantumRegister(5)
        self.qc = QuantumCircuit(qr, qr_target, name='initialize_oracle_part')

        for edge in distances:
            if edge[0] == '3':
                node = format(int(edge[1]), '02b')
                d_bin = format(distances[edge], '02b')

                for idx in range(len(node)):
                    if node[idx] == '0':
                        self.qc.x(qr[idx])

                for idx in range(len(d_bin)):
                    if d_bin[idx] == '1':
                        self.qc.ccx(qr[0], qr[1], qr_target[idx])

                for idx in range(len(node)):
                    if node[idx] == '0':
                        self.qc.x(qr[idx])

        return self.qc

    def dist():
        """Enter method docstring here"""
        qr1 = QuantumRegister(2)
        qr2 = QuantumRegister(2)
        qr_target = QuantumRegister(5)
        qr_anc = QuantumRegister(2)
        self.qc = QuantumCircuit(qr1, qr2, qr_target, qr_anc, name='dist')

        for edge in distances:
            if edge[0] != '3':
                # convert to binaries
                node1 = format(int(edge[0]), '02b')
                node2 = format(int(edge[1]), '02b')
                d_bin = format(distances[edge], '02b')

                for idx in range(len(node1)): # assume node1 and node2 have the same length
                    if node1[idx] == '0':
                        self.qc.x(qr1[idx])

                for idx in range(len(node2)):
                    if node2[idx] == '0':
                        self.qc.x(qr2[idx])

                for idx in range(len(d_bin)):
                    if d_bin[idx] == '1':
                        self.qc.mct(qr1[:]+qr2[:], qr_target[idx], qr_anc)

                for idx in range(len(node2)): # invert back
                    if node2[idx] == '0':
                        self.qc.x(qr2[idx])

                for idx in range(len(node1)):
                    if node1[idx] == '0':
                        self.qc.x(qr1[idx])

        return self.qc
        
    ## multiple adder

    def maj(self, a, b, k):
        """Enter method docstring here"""
        self.qc.cx(q[k], q[b])
        self.qc.cx(q[k], q[a])
        self.qc.ccx(q[a], q[b], q[k])

    def unmaj(self, a, b, k):
        """Enter method docstring here"""
        self.qc.ccx(q[a], q[b], q[k])
        self.qc.cx(q[k], q[a])
        self.qc.cx(q[a], q[b])

    def multiple_adder(self, a, b, c_0, z):
        """Enter method docstring here"""
        arr_size = len(a)
        maj(c_0, b[0], a[0])
        for i in range(arr_size-1):
            maj(a[i], b[i+1], a[i+1])
        self.qc.cx(q[a[arr_size-1]], q[z])
        for i in reversed(range(arr_size-1)):
            unmaj(a[i], b[i+1], a[i+1])
        unmaj(c_0, b[0], a[0])
    
    ## self.diffusion
    
    def diffusion(self):
        """Enter method docstring here"""
        self.qc.h(q[0:6])
        self.qc.x(q[0:6])
        self.qc.h(q[5])
        self.qc.barrier()
        self.qc.mct(q[0:5], q[5], q[7:10])
        self.qc.barrier()
        self.qc.h(q[5])
        self.qc.x(q[0:6])
        self.qc.h(q[0:6])
        
    def solve_tsp(self, coordinates: np.ndarray = None) -> dict:
        """
        Optimizes the travelling salesman problem with Grover's algorithm for
        the given coordinates.
        """
        
        ## build everything
        
        qubit_num = 25  # max is 32 if you're using the simulator

        # ancilla indices
        inputs = [0, 1, 2, 3, 4, 5]
        init_ancillae = [6, 7, 8, 9]
        valid = [10]
        temp_dist = [11, 12, 13, 14, 15]
        total_dist = [16, 17, 18, 19, 20]
        gate_ancillae = [21, 22, 23]
        check_dist = [11, 12, 13, 14, 15] # initialize 13 here
        carry_check = [24]

        inputs = inputs[0]
        init_ancillae = init_ancillae[0]
        valid = valid[0]
        temp_dist = temp_dist[0]
        total_dist = total_dist[0]
        gate_ancillae = gate_ancillae[0]
        check_dist = check_dist[0]
        carry_check = carry_check[0]

        q = QuantumRegister(qubit_num)
        c = ClassicalRegister(6)
        self.qc = QuantumCircuit(q, c)

        self.qc.h(q[0:6])
        self.qc.x(q[carry_check])

        # forward oracle
        self.initialize_oracle_part(4)
        self.qc.append(self.initialize_oracle_part(), q[inputs:inputs+2] + q[temp_dist:temp_dist+5])
        multiple_adder([11, 12, 13, 14], [16, 17, 18, 19], init_ancillae, 20)
        self.qc.append(self.initialize_oracle_part().inverse(), q[inputs:inputs+2] + q[temp_dist:temp_dist+5])
        self.qc.append(dist(), q[inputs:inputs+4] + q[temp_dist:temp_dist+5] + q[gate_ancillae:gate_ancillae+2])
        multiple_adder([11, 12, 13, 14], [16, 17, 18, 19], init_ancillae, 20)
        self.qc.append(dist().inverse(), q[inputs:inputs+4] + q[temp_dist:temp_dist+5] + q[gate_ancillae:gate_ancillae+2])
        self.qc.append(dist(), q[inputs+2:inputs+6] + q[temp_dist:temp_dist+5] + q[gate_ancillae:gate_ancillae+2])
        multiple_adder([11, 12, 13, 14], [16, 17, 18, 19], init_ancillae, 20)
        self.qc.append(dist().inverse(), q[inputs+2:inputs+6] + q[temp_dist:temp_dist+5] + q[gate_ancillae:gate_ancillae+2])
        self.qc.x(q[check_dist:check_dist+3]) # init 15
        multiple_adder([11, 12, 13, 14, 15], [16, 17, 18, 19, 20], init_ancillae, carry_check)

        # carry_check
        self.qc.barrier()
        self.qc.cz(q[valid], q[carry_check])
        self.qc.barrier()

        # inverse oracle
        multiple_adder([11, 12, 13, 14, 15], [16, 17, 18, 19, 20], init_ancillae, carry_check)
        self.qc.x(q[check_dist:check_dist+3]) # init 15
        self.qc.append(dist().inverse(), q[inputs+2:inputs+6] + q[temp_dist:temp_dist+5] + q[gate_ancillae:gate_ancillae+2])
        multiple_adder([11, 12, 13, 14], [16, 17, 18, 19], init_ancillae, 20)
        self.qc.append(dist(), q[inputs+2:inputs+6] + q[temp_dist:temp_dist+5] + q[gate_ancillae:gate_ancillae+2])
        self.qc.append(dist().inverse(), q[inputs:inputs+4] + q[temp_dist:temp_dist+5] + q[gate_ancillae:gate_ancillae+2])
        multiple_adder([11, 12, 13, 14], [16, 17, 18, 19], init_ancillae, 20)
        self.qc.append(dist(), q[inputs:inputs+4] + q[temp_dist:temp_dist+5] + q[gate_ancillae:gate_ancillae+2])
        self.qc.append(self.initialize_oracle_part().inverse(), q[inputs:inputs+2] + q[temp_dist:temp_dist+5])
        multiple_adder([11, 12, 13, 14], [16, 17, 18, 19], init_ancillae, 20)
        self.qc.append(self.initialize_oracle_part(), q[inputs:inputs+2] + q[temp_dist:temp_dist+5])
        self.initialize_oracle_part(4)

        self.self.diffusion()

        self.qc.measure(q[:6], c)
        self.qc.draw()
        
        ## execution
        
        pass_ = Unroller(['u3', 'cx'])
        pm = PassManager(pass_)
        new_circuit = pm.run(self.qc)
        print(new_circuit.count_ops())
        backend = Aer.get_backend('qasm_simulator')
        job = execute(self.qc, backend, shots=1024)
        counts = job.result().get_counts()
        
        ## show results
        
        print(sorted(counts.items(), key=lambda x:x[1], reverse=True)[0:20])
        plot_histogram(counts)
