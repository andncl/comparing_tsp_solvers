"""Module containing QuantumPhaseEstimator class"""
import copy
import time
from importlib import reload

import numpy as np
import matplotlib.pyplot as plt

from dwave.embedding.chain_strength import scaled
from dwave.system.composites import EmbeddingComposite
from dwave.system.samplers import DWaveSampler
import dwave.inspector


from .tsp_solver_base import TspSolverBase

class QuantumAnnealer(TspSolverBase):
    """ 
    The QuantumAnnealer class formulates and solves the traveling salesman
    problem with the quantum aealing algorithm with D-waves ocean SDKs
    """
    def __init__(self) -> None:
        """Constructor class of QuantumAnnealer class"""
        super().__init__()
        self.qubo = None # Q + lagrange_multiplier * C
        self.sampler = EmbeddingComposite(DWaveSampler()) 

    def generate_qubo_matrix_from_cities(self, nr_cities: int):
        """Generates a QUBO matrix from a given set of cites on a map
        
        Args:
            nr_cities (int): Number of cities to solve TSP for
        """
        self.set_cities_coordinates(nr_of_cities=nr_cities)
    def solve_tsp(self, coordinates):
        t0 = time.perf_counter()
        sampleset = self.sampler.sample_qubo(
            qubo, 
            num_reads=num_samples,
            chain_strength=scaled
            )
        t1 = time.perf_counter()
        return t1-t0

    def 
    def show_result(self):
        """Shows calculated sample set"""
        dwave.inspector.show(sampleset)