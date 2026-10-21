import os
import sys
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from search import breadth_first_search


class BreadthFirstSearchTests(unittest.TestCase):
    def test_finds_shortest_path(self):
        allowed = {(x, y) for x in range(4) for y in range(3)}
        path = breadth_first_search((0, 0), (3, 0), allowed)
        self.assertEqual(len(path), 3)

    def test_routes_around_blocked_cell(self):
        allowed = {(x, y) for x in range(3) for y in range(3)}
        allowed.remove((1, 0))
        path = breadth_first_search((0, 0), (2, 0), allowed)
        self.assertIsNotNone(path)
        self.assertGreater(len(path), 2)

    def test_returns_none_when_goal_unreachable(self):
        allowed = {(0, 0), (1, 0), (3, 0)}
        self.assertIsNone(breadth_first_search((0, 0), (3, 0), allowed))

    def test_start_equals_goal(self):
        self.assertEqual(breadth_first_search((1, 1), (1, 1), {(1, 1)}), [])


if __name__ == "__main__":
    unittest.main()
