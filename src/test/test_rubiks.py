import unittest
import pycuber as pc
import sys
import random

sys.path.insert(0, "src/utils")
from rubiks_utils import *


class RubiksTestSuite(unittest.TestCase):

    def test_cube_to_config_1(self):
        # 100 random test cases
        for _ in range(100):
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

    
    def test_config_to_cube_1(self):
        # Test with 100 random formulas
        for _ in range(100):
            formula = pc.Formula().random(random.randint(1, 10))
            cube1 = pc.Cube()
            cube2 = config_to_cube("UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDBBBBBBBBBLLLLLLLLL")
            self.assertEqual(cube1, cube2)

            # Apply formula to both cubes
            cube1(formula)
            cube2(formula)

            self.assertEqual(cube1, cube2)

    
    def test_config_to_cube_2(self):
        # Create random configs from random cubes and ensure that the resulting cubes are valid (solvable)
        # Test with 100 random formulas
        for _ in range(100):
            formula = pc.Formula().random(random.randint(1, 20))
            cube = pc.Cube()
            cube(formula)
            config = get_config_string(cube)
            # Build second cube directly from this config string
            cube2 = config_to_cube(config)
            # Ensure this second cube is valid
            self.assertTrue(cube2.is_valid())


if __name__ == "__main__":
    unittest.main()