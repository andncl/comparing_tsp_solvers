import pytest
from src.tsp_solver_base import TspSolverBase

@pytest.fixture
def dummy_solver():
    yield TspSolverBase()