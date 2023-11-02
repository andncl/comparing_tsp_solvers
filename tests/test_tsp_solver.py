"""Module containing pytests for `TspSolverBase`"""
import pytest
import numpy as np

from src.tsp_solver_base import TspSolverBase

@pytest.mark.parametrize(
    "nr_cities,size",
    [[4,10], [10,45], [57, 31]]
)
def test_cities_property(nr_cities, size, dummy_solver):
    cities = dummy_solver.set_cities_coordinates(nr_cities, size)
    assert dummy_solver.cities == cities
    other_cities = {'0': np.array([0,0])}
    dummy_solver.cities = other_cities
    assert other_cities == dummy_solver.cities

@pytest.mark.parametrize(
    "nr_cities,size",
    [[3,8], [7,8], [9,12], [99, 57]])
def test_set_cities_coordinates(nr_cities, size, dummy_solver):
    """Tests if `set_cities_coordinates` generaters cities correctly"""
    cities = dummy_solver.set_cities_coordinates(nr_cities, grid_size = size)
    print(cities)
    assert isinstance(cities, dict)
    assert all(len(coord) for coord in cities.values())
    print(set(list(range(len(cities)))), list(cities.keys()))
    all_cities = [str(city) for city in range(len(cities))]
    assert set(all_cities).issubset(list(cities.keys()))
    for coords in cities.values():
        assert all(coord < size for coord in coords)

@pytest.mark.parametrize(
    "city_dict,inter_dist,sequence,dist",
    [
        [
            {'0': np.array([0,0]), '1': np.array([3,4]), '2':np.array([0,4])},
            {'10': 5, '20': 4, '21': 3},
            '012',
            5+3+4
        ],
        [
            {'0': np.array([0,0]), '1': np.array([0,0]), '2':np.array([0,0])},
            {'10': 0, '20': 0, '21': 0},
            '012',
            0
        ],
        [
            {
                '0': np.array([0,0]),
                '1': np.array([0,10]),
                '2': np.array([10,10]),
                '3': np.array([10,0])
            },
            {'10': 10, '20': 14, '30': 10,'21': 10, '31': 14, '32': 10},
            '0123',
            40
        ],
        [
            {'0': np.array([0,0]), '1': np.array([1,1])},
            {'10': 1},
            '01',
            2
        ]
    ]
    )
def test_get_total_travel_distance(
    city_dict, inter_dist, sequence, dist, dummy_solver):
    """
    Tests 3 implementations at the same time:

        1) Tests if `get_total_travel_distance` returns the correct total
            distances
        2) Tests if `calculate_distances` returns the correct inter-city 
            distances
        3) Tests if for each subset of city pairs the correct inter city
            distance is returned by `get_inter_city_distance`
    """
    dummy_solver.cities = city_dict
    distance = dummy_solver.get_total_travel_distance(sequence)
    assert distance == dist
    inter_city_dist = dummy_solver.calculate_distances(city_dict)
    assert inter_city_dist == inter_dist

@pytest.mark.parametrize(
    "sequence,nr_cities,valid",
    [
        ["0123", 4, True],
        ["0123", 3, False],
        ["0112", 4, False],
        ["312", 4, False],
        ["3102", 4, True],
        ["4210", 4, False],
        ["012345", 6, True],
        ["012345", 3, False],
        ])
def test_is_sequence_valid(sequence, nr_cities, valid,  dummy_solver):
    """Tests whether `is_sequence_valid` detects valid sequences"""
    dummy_solver.set_cities_coordinates(nr_cities, 10)
    assert dummy_solver.is_sequence_valid(sequence) == valid
