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

    Attributes:
        self.q (None | qiskit.QuantumRegister):
        self.c (None | qiskit.ClassicalRegister):
        self.qc (None | qiskit.QuantumCircuit):
        self.distances (list): list of inter city distances
    """
    def __init__(self) -> None:
        """Constructor method of Grover class"""
        super().__init__()
        self.c = None 
        self.q = None 
        self.qc = None
        self.distances = None


    def OR(self, qubit_1: int, qubit_2, k: int) -> None:
        """ 
        Function does the equivalent of a classical OR between qubit_1 and
        qubit_2, sand stores the result in qubit number k.
        
        Args:
            qubit_1 (int): Index of qubit 1
            qubit_2 (int): Index of qubit 2
        """
        self.qc.x(self.q[qubit_1])
        self.qc.x(self.q[qubit_2])
        self.qc.ccx(self.q[qubit_1], self.q[qubit_2], self.q[k])
        self.qc.x(self.q[k])
        self.qc.x(self.q[qubit_1])
        self.qc.x(self.q[qubit_2])


    def are_not_equal(self, a_0: int, b_0: int, k: int):
        """
        Function outputs 1 if nodes a and b are not the same. Node numbering 
        starts from 0 as in the problem statement. k is the output qubit where 
        the output is XOR-ed. qubit numbering also starts from 0.
        
        Args:
            a_0 (int): node number
            b_0 (int): node number
            k (int): output qubit

        """
        self.qc.cx(self.q[2*a_0], self.q[2*b_0])
        self.qc.cx(self.q[(2*a_0) + 1], self.q[(2*b_0) + 1])
        self.OR(2*b_0, (2*b_0)+1, k)
        self.qc.cx(self.q[2*a_0], self.q[2*b_0])
        self.qc.cx(self.q[(2*a_0) + 1], self.q[(2*b_0) + 1])

    def is_not_3(self, a: int, k: int):
        """
        Function outputs 1 if the number represented by qubits 2a and 2a+1 is 
        not equal to 3. Node numbering starts from 0 as in the problem 
        statement. k is the qubit where the output is stored.
        
        Args:
            a (int): node number
            k (int): output qubit

        """
        self.qc.ccx(self.q[2*a], self.q[(2*a)+1], self.q[k])
        self.qc.x(self.q[k])

    def initialize_oracle(self, n: int = None):
        """
        Initial oracle to mark the validated routes
        
        Args:
            None
            
        """
        self.are_not_equal(0, 1, 6) # node a and b are not equal 
        self.are_not_equal(0, 2, 7)
        self.are_not_equal(1, 2, 8)
        self.is_not_3(0, 11)
        self.is_not_3(1, 12)
        self.is_not_3(2, 13)
        self.qc.mct(
            [self.q[6], self.q[7], self.q[8], self.q[11], self.q[12], self.q[13]],
            self.q[10],
            [self.q[9], self.q[14], self.q[15], self.q[16]]
            )
        # answer is stored in 10. keep 9 a clean qubit, it's used as 
        # ancilla here 
        self.is_not_3(0, 11)
        self.is_not_3(1, 12)
        self.is_not_3(2, 13)
        self.are_not_equal(0, 1, 6) # node a and b are not equal 
        self.are_not_equal(0, 2, 7)
        self.are_not_equal(1, 2, 8)
        
    ## distance_black_box, needs to become user-defined in next version

    def dist_single(self):
        """
        Add 4 to a distance
        
        Args:
            qc: distance sum
        Returns:
            qiskit.QuantumCircuit: Circuit for dist_single oracle
        """
        qr = QuantumRegister(2)
        qr_target = QuantumRegister(5)
        qc = QuantumCircuit(qr, qr_target, name='dist_single')

        for edge in self.distances:
            if edge[0] == '3':
                node = format(int(edge[1]), '02b')
                d_bin = format(self.distances[edge], '02b')

                for idx in range(len(node)):
                    if node[idx] == '0':
                        qc.x(qr[idx])

                for idx in range(len(d_bin)):
                    if d_bin[idx] == '1':
                        qc.ccx(qr[0], qr[1], qr_target[idx])

                for idx in range(len(node)):
                    if node[idx] == '0':
                        qc.x(qr[idx])

        return qc

    def dist(self):
        """
        Adds 2 distances
        
        Args:
            qc: distance sum

        Returns:
            qiskit.QuantumCircuit: Circuit for dist oracle
        """
        qr1 = QuantumRegister(2)
        qr2 = QuantumRegister(2)
        qr_target = QuantumRegister(5)
        qr_anc = QuantumRegister(2)
        qc = QuantumCircuit(qr1, qr2, qr_target, qr_anc, name='dist')

        for edge in self.distances:
            if edge[0] != '3':
                # convert to binaries
                node1 = format(int(edge[0]), '02b')
                node2 = format(int(edge[1]), '02b')
                d_bin = format(self.distances[edge], '02b')
                # assume node1 and node2 have the same length
                for idx in range(len(node1)): 
                    if node1[idx] == '0':
                        qc.x(qr1[idx])

                for idx in range(len(node2)):
                    if node2[idx] == '0':
                        qc.x(qr2[idx])

                for idx in range(len(d_bin)):
                    if d_bin[idx] == '1':
                        qc.mct(qr1[:]+qr2[:], qr_target[idx], qr_anc)

                for idx in range(len(node2)): # invert back
                    if node2[idx] == '0':
                        qc.x(qr2[idx])

                for idx in range(len(node1)):
                    if node1[idx] == '0':
                        qc.x(qr1[idx])
        return qc

    ## multiple adder
    def maj(self, a, b, k):
        """
        Majority function,
        MAJ|c⟩|b⟩|a⟩ = |c⊕a⟩|b⊕a⟩|c′⟩
        
        Args:
            a (int): node number
            b (int): node number
            k (int): output qubit

        """
        self.qc.cx(self.q[k], self.q[b])
        self.qc.cx(self.q[k], self.q[a])
        self.qc.ccx(self.q[a], self.q[b], self.q[k])

    def unmaj(self, a, b, k):
        """
        Un-majority function,
        UMAJ|c⟩|b⟩|a⟩ = |c⊕a⟩|b⊕a⟩|c′⟩
        
        Args:
            a (int): node number
            b (int): node number
            k (int): output qubit
            
        """
        self.qc.ccx(self.q[a], self.q[b], self.q[k])
        self.qc.cx(self.q[k], self.q[a])
        self.qc.cx(self.q[a], self.q[b])

    def multiple_adder(self, a, b, c_0, z):
        """
        Adder
        
        Args:
            a (int): node number
            b (int): node number
            c_0 (int): carry
            z: sum
            
        """
        arr_size = len(a)
        self.maj(c_0, b[0], a[0])
        for i in range(arr_size-1):
            self.maj(a = a[i], b = b[i+1], k = a[i+1])
        self.qc.cx(self.q[a[arr_size-1]], self.q[z])
        for i in reversed(range(arr_size-1)):
            self.unmaj(a[i], b[i+1], a[i+1])
        self.unmaj(c_0, b[0], a[0])
    
    def diffusion(self):
        """
        Diffusion operation for amplitude amplification
        
        Args:
            None
            
        """
        self.qc.h(self.q[0:6])
        self.qc.x(self.q[0:6])
        self.qc.h(self.q[5])
        self.qc.barrier()
        self.qc.mct(self.q[0:5], self.q[5], self.q[7:10])
        self.qc.barrier()
        self.qc.h(self.q[5])
        self.qc.x(self.q[0:6])
        self.qc.h(self.q[0:6])


    
    def solve_tsp(self, cities: dict, verbose: bool = False) -> dict:
        """
        Optimises the travelling salesman problem with Grover's algorithm for
        the given coordinates.

        Args:
            cities (dict): cities to solve the TSP for
            verbose (bool): Whether the 20 best states are printed after solving

        Returns:
            str: String of cities that represent the solved sequence

        Raises:
            ValueError: If the given dict of cities is not eual to 4
        """
        qubit_num = 25  # max is 32 if you're using the simulator
        if len(cities) is not 4:
            raise ValueError("This algorithm supports 4 only cities!")
        self.distances = self.calculate_distances(cities)
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

        self.q = QuantumRegister(qubit_num)
        self.c = ClassicalRegister(6)
        self.qc = QuantumCircuit(self.q, self.c)

        self.qc.h(self.q[0:6])
        self.qc.x(self.q[carry_check])

        # forward oracle
        self.initialize_oracle(4)
        self.qc.append(
            self.dist_single(),
            self.q[inputs:inputs+2] + self.q[temp_dist:temp_dist+5]
            )
        self.multiple_adder(
            a = [11, 12, 13, 14],
            b = [16, 17, 18, 19],
            c_0 = init_ancillae,
            z = 20
            )
        self.qc.append(
            self.dist_single().inverse(),
            self.q[inputs:inputs+2] + self.q[temp_dist:temp_dist+5]
            )
        self.qc.append(
            self.dist(),
            self.q[inputs:inputs+4] + self.q[temp_dist:temp_dist+5] +
            self.q[gate_ancillae:gate_ancillae+2]
            )
        self.multiple_adder(
            [11, 12, 13, 14],
            [16, 17, 18, 19],
            init_ancillae,
            20
            )
        self.qc.append(
            self.dist().inverse(),
            self.q[inputs:inputs+4] + self.q[temp_dist:temp_dist+5] +
            self.q[gate_ancillae:gate_ancillae+2]
            )
        self.qc.append(
            self.dist(),
            self.q[inputs+2:inputs+6] + self.q[temp_dist:temp_dist+5] +
            self.q[gate_ancillae:gate_ancillae+2]
            )
        self.multiple_adder(
            [11, 12, 13, 14], [16, 17, 18, 19], init_ancillae, 20)
        self.qc.append(
            self.dist().inverse(),
            self.q[inputs+2:inputs+6] + self.q[temp_dist:temp_dist+5] +
            self.q[gate_ancillae:gate_ancillae+2]
            )
        self.qc.x(self.q[check_dist:check_dist+3]) # init 15
        self.multiple_adder(
            [11, 12, 13, 14, 15],
            [16, 17, 18, 19, 20],
            init_ancillae,
            carry_check
            )

        # carry_check
        self.qc.barrier()
        self.qc.cz(self.q[valid], self.q[carry_check])
        self.qc.barrier()

        # inverse oracle
        self.multiple_adder(
            [11, 12, 13, 14, 15],
            [16, 17, 18, 19, 20],
            init_ancillae,
            carry_check
            )
        self.qc.x(self.q[check_dist:check_dist+3]) # init 15
        self.qc.append(
            self.dist().inverse(),
            self.q[inputs+2:inputs+6] + self.q[temp_dist:temp_dist+5] +
            self.q[gate_ancillae:gate_ancillae+2]
            )
        self.multiple_adder(
            [11, 12, 13, 14],
            [16, 17, 18, 19],
            init_ancillae,
            20
            )
        self.qc.append(
            self.dist(),
            self.q[inputs+2:inputs+6] + self.q[temp_dist:temp_dist+5] +
            self.q[gate_ancillae:gate_ancillae+2]
            )
        self.qc.append(
            self.dist().inverse(),
            self.q[inputs:inputs+4] + self.q[temp_dist:temp_dist+5] +
            self.q[gate_ancillae:gate_ancillae+2]
            )
        self.multiple_adder(
            [11, 12, 13, 14],
            [16, 17, 18, 19],
            init_ancillae,
            20
            )
        self.qc.append(
            self.dist(),
            self.q[inputs:inputs+4] + self.q[temp_dist:temp_dist+5] +
            self.q[gate_ancillae:gate_ancillae+2]
            )
        self.qc.append(
            self.dist_single().inverse(),
            self.q[inputs:inputs+2] + self.q[temp_dist:temp_dist+5]
            )
        self.multiple_adder(
            [11, 12, 13, 14],
            [16, 17, 18, 19],
            init_ancillae,
            20
            )
        self.qc.append(
            self.dist_single(),
            self.q[inputs:inputs+2] + self.q[temp_dist:temp_dist+5]
            )
        self.initialize_oracle(4)
        self.diffusion()

        self.qc.measure(self.q[:6], self.c)
        self.qc.draw()
        
        ## execution
        
        pass_ = Unroller(['u3', 'cx'])
        pm = PassManager(pass_)
        new_circuit = pm.run(self.qc)
        #print(f"New circuit: {new_circuit.count_ops()}")
        backend = Aer.get_backend('qasm_simulator')
        job = execute(self.qc, backend, shots=1024)
        counts = job.result().get_counts()
        
        ## show results
        sorted_states_bin = sorted(
            counts.items(), key=lambda x:x[1], reverse=True)[0:20]
        sorted_states_dec = []
        for state in sorted_states_bin:
            decimal_result = self.convert_binary_to_decimal_result(state[0])
            sorted_states_dec.append((
                    decimal_result,
                    state[1],
                    self.get_total_travel_distance(str(decimal_result))
                    )
            )
        if verbose:
            print(f"RESULT_bin: {sorted_states_bin}")
            print(f"RESULT_dec: {sorted_states_dec}")
        plot_histogram(counts)
        return sorted_states_dec[0][0]

    def convert_binary_to_decimal_result(self, bin_result):
        """
        Converts the given binary result to a decimal result

        Args:
            bin_result (str): Binary sequence encoding the given order

        Returns:
            str: Decimal sequence of cities
        """
        dec=  [int(bin_result[i:i+2], 2) for i in range(0, len(bin_result), 2)]
        return '0'+''.join(str(x+1) for x in dec)
