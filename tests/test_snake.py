import unittest

from games.snake_game import check_collision, move_snake


class SnakeGameLogicTests(unittest.TestCase):
    def test_move_snake_forward(self):
        snake = [(3, 3), (2, 3), (1, 3)]
        result = move_snake(snake, (1, 0))
        self.assertEqual(result, [(4, 3), (3, 3), (2, 3)])

    def test_collision_with_wall(self):
        snake = [(0, 0), (0, 1)]
        self.assertTrue(check_collision(snake, width=10, height=10))

    def test_no_collision_inside_board(self):
        snake = [(3, 3), (2, 3)]
        self.assertFalse(check_collision(snake, width=10, height=10))


if __name__ == "__main__":
    unittest.main()
