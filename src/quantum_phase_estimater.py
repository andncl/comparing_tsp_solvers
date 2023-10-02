"""Module containing QuantumPhaseEstimator class"""
import copy
import logging

import numpy as np
import matplotlib.pyplot as plt

from .tsp_solver_base import TspSolverBase

class QuantumPhaseEstimator(TspSolverBase):
    """ 
    The SimulatedAnnealer class formulates and solves the traveling salesman
    problem with the classical simulated annealing algorithm
    """
    def __init__(self) -> None:
        super().__init__()

    def solve_tsp(self, coordinates: np.ndarray = None) -> dict:
        """
        Optimizes the travelling salesman problem with simulated annealing for
        the given coordinates.
        """