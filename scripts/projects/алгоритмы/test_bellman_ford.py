#test_bellman_ford.py
import pytest
from bellman_ford_module import BellmanFord

def test_simple_graph():
    V = 5
    E = [
        (0, 1, -1),
        (0, 2,  4),
        (1, 2,  3),
        (1, 3,  2),
        (1, 4,  2),
        (3, 2,  5),
        (3, 1,  1),
        (4, 3, -3)
    ]
    bf = BellmanFord(V, E, 0)
    distances = bf.run()
    assert distances == [0, -1, 2, -2, 1]
    assert bf.get_path(3) == [0, 1, 4, 3]

def test_negative_cycle():
    V = 3
    E = [
        (0, 1, 1),
        (1, 2, -1),
        (2, 0, -1)
    ]
    bf = BellmanFord(V, E, 0)
    with pytest.raises(ValueError):
        bf.run()
