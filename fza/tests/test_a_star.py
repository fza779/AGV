import unittest

from fza.services.a_star import a_star


class AStarTests(unittest.TestCase):
    def test_straight_path(self):
        grid = [[0, 0, 0, 0]]

        result = a_star(grid, [0, 0], [0, 3])

        self.assertTrue(result["success"])
        self.assertEqual(result["path"], [[0, 0], [0, 1], [0, 2], [0, 3]])
        self.assertEqual(result["cost"], 3.0)

    def test_path_around_obstacle(self):
        grid = [
            [0, 0, 0],
            [1, 1, 0],
            [0, 0, 0],
        ]

        result = a_star(grid, [0, 0], [2, 2])

        self.assertTrue(result["success"])
        self.assertEqual(result["path"][0], [0, 0])
        self.assertEqual(result["path"][-1], [2, 2])
        self.assertEqual(result["cost"], 4.0)

    def test_no_path(self):
        grid = [[0, 1, 0]]

        result = a_star(grid, [0, 0], [0, 2])

        self.assertFalse(result["success"])
        self.assertEqual(result["path"], [])

    def test_start_equals_goal(self):
        grid = [[0, 0], [0, 0]]

        result = a_star(grid, [1, 1], [1, 1])

        self.assertTrue(result["success"])
        self.assertEqual(result["path"], [[1, 1]])
        self.assertEqual(result["cost"], 0.0)

    def test_diagonal_cannot_cut_obstacle_corner(self):
        grid = [
            [0, 1],
            [1, 0],
        ]

        result = a_star(grid, [0, 0], [1, 1], allow_diagonal=True)

        self.assertFalse(result["success"])


if __name__ == "__main__":
    unittest.main()
