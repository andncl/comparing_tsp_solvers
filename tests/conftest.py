import pytest
from src.tsp_solver_base import TspSolverBase

class DummySolver(TspSolverBase):
    def solve_tsp(self, coordinates):        
        return None

@pytest.fixture
def dummy_solver():
    yield DummySolver()