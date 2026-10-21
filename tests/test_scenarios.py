import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from scenarios import create_scenario


class ScenarioTests(unittest.TestCase):
    def test_scenario_2_obstacles_are_between_10_and_50_percent(self):
        width, height = 20, 15
        scenario = create_scenario(2, width, height, seed=123)
        count = len(scenario["obstacles"])
        total = width * height
        self.assertGreaterEqual(count / total, 0.10)
        self.assertLessEqual(count / total, 0.50)
        self.assertTrue(scenario["obstacles"].isdisjoint(scenario["snake"]))
        self.assertNotIn(scenario["food"], scenario["obstacles"])

    def test_scenario_2_seed_reproduces_layout(self):
        a = create_scenario(2, 20, 15, seed=42)
        b = create_scenario(2, 20, 15, seed=42)
        self.assertEqual(a["obstacles"], b["obstacles"])

    def test_scenario_3_fruit_is_inside_closed_chamber(self):
        scenario = create_scenario(3, 20, 15)
        food = scenario["food"]
        obstacles = scenario["obstacles"]
        self.assertNotIn(food, obstacles)
        self.assertNotIn(food, scenario["snake"])
        x, y = food
        self.assertIn((x - 1, y), obstacles)
        self.assertIn((x + 1, y), obstacles)
        self.assertIn((x, y - 1), obstacles)
        self.assertIn((x, y + 1), obstacles)
        self.assertTrue(obstacles.isdisjoint(scenario["snake"]))

    def test_scenario_3_requires_minimum_size(self):
        with self.assertRaises(ValueError):
            create_scenario(3, 6, 6)

    def test_scenario_3_works_at_minimum_size(self):
        scenario = create_scenario(3, 7, 7)
        self.assertTrue(scenario["obstacles"].isdisjoint(scenario["snake"]))
        self.assertNotIn(scenario["food"], scenario["snake"])
        self.assertNotIn(scenario["food"], scenario["obstacles"])


if __name__ == "__main__":
    unittest.main()
