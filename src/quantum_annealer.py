"""Module containing QuantumPhaseEstimator class"""
import copy
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

    def solve_tsp(self, coordinates):
        return super().solve_tsp(coordinates)