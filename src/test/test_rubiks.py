import unittest
import pycuber as pc
import sys
import random

sys.path.insert(0, "src\data")
from generate_rubiks_data import *

sys.path.insert(0, "src\model")
from test_rubiks import *


class RubiksTestSuite(unittest.TestCase):

    def test_cube_conversions(self):
        # 20 random test cases
        for _ in range(20):
            # Create new cube
            cube = pc.Cube()
            # Create random formula
            formula = gen_init_config(random.randint(1, 20))
            # Apply formula to cube
            cube(formula)
            # Get config string for cube
            config = get_config_string(cube)
            # Use config string to build second cube
            cube2 = config_to_cube(config)

            # Assert that cubes are identical
            self.assertEqual(cube, cube2)


if __name__ == "__main__":
    unittest.main()