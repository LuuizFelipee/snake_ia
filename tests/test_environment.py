import unittest
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from environment import SnakeEnvironment

class EnvironmentTests(unittest.TestCase):
    def test_snake_moves(self):
        env = SnakeEnvironment(10, 8, initial_snake=[(3, 3), (2, 3), (1, 3)], initial_food=(8, 6))
        result = env.step("RIGHT")
        self.assertTrue(result.moved)
        self.assertEqual(env.snake[0], (4, 3))
        self.assertEqual(len(env.snake), 3)

    def test_eating_grows(self):
        env = SnakeEnvironment(10, 8, initial_snake=[(3, 3), (2, 3), (1, 3)], initial_food=(4, 3), seed=1)
        result = env.step("RIGHT")
        self.assertTrue(result.ate_food)
        self.assertEqual(len(env.snake), 4)
        self.assertEqual(env.score, 1)

    def test_wall_collision(self):
        env = SnakeEnvironment(6, 6, initial_snake=[(5, 2), (4, 2), (3, 2)], initial_food=(1, 1))
        result = env.step("RIGHT")
        self.assertEqual(result.collision, "parede")
        self.assertTrue(env.game_over)

    def test_tail_cell_can_be_entered(self):
        env = SnakeEnvironment(6, 6, initial_snake=[(2, 2), (2, 3), (1, 3), (1, 2)], initial_food=(4, 4))
        env.direction = "UP"  # LEFT não é reversão imediata de UP
        result = env.step("LEFT")
        self.assertTrue(result.moved)
        self.assertEqual(env.snake[0], (1, 2))

if __name__ == "__main__":
    unittest.main()
