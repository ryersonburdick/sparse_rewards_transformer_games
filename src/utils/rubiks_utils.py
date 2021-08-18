"""Utility functions for processing Rubik's data."""

import pycuber as pc
from pycuber import Corner, Edge, Centre, Square
from pycuber.solver import CFOPSolver
import random


# Rubik's constants
COLORS = ['red', 'blue', 'yellow', 'white', 'green', 'orange']
FACES = ["U", "R", "F", "D", "B", "L"]
# Standard traversal order for all faces on a cube,
# faces indexed by cube[cubie][face]
FACES_ORDER = ["U"] * 9
FACES_ORDER.extend(["R"] * 9)
FACES_ORDER.extend(["F"] * 9)
FACES_ORDER.extend(["D"] * 9)
FACES_ORDER.extend(["B"] * 9)
FACES_ORDER.extend(["L"] * 9)
CUBIES_ORDER = ["".join(sorted(s)) for s in [
    "ULB", "UB", "URB", "UL", "U", "UR", "ULF", "UF", "URF", 
    "URF", "UR", "URB", "RF", "R", "RB", "RFD", "RD", "RDB", 
    "UFL", "UF", "UFR", "FL", "F", "FR", "FLD", "FD", "FRD", 
    "DFL", "DF", "DFR", "DL", "D", "DR", "DLB", "DB", "DRB", 
    "URB", "UB", "ULB", "BR", "B", "BL", "BRD", "BD", "BLD", 
    "ULB", "UL", "ULF", "LB", "L", "LF", "LBD", "LD", "LFD"
]]


def get_map_colors_to_faces(cube):
    """Return a dict which maps color names to faces for a specified Cube."""
    
    colors_to_faces = {}
    for color in COLORS:
        face = cube.which_face(color)
        colors_to_faces[color] = face
    return colors_to_faces


def get_map_faces_to_colors(cube):
    """Return a dict which maps faces to color names for a specified Cube."""
    
    faces_to_colors = {}
    for color in COLORS:
        face = cube.which_face(color)
        faces_to_colors[face] = color
    return faces_to_colors


def config_to_cube(config):
    """Given a config string (9*(URFDBL)), produce a PyCuber.Cube object."""

    # Replace whitespace in config string
    config = config.replace(" ", "")

    # Get list of colors for all faces in standard traversal order
    faces_to_colors = get_map_faces_to_colors(pc.Cube())
    colors_list = [faces_to_colors[face] for face in config]

    # Create dict mapping cubie ID->face ID->color
    cubies_dict = {cubie:{} for cubie in CUBIES_ORDER}
    for color, cubie, face in zip(colors_list, CUBIES_ORDER, FACES_ORDER):
        cubies_dict[cubie][face] = color
    
    # Use dict of cubie to create set of cubies which will be used to create final cube
    cubies = set()
    for cubie_id in cubies_dict.keys():
        # Corner cubie touches 3 faces
        if len(cubie_id) == 3:
            new_cubie = Corner(**{f:Square(cubies_dict[cubie_id][f]) for f in cubies_dict[cubie_id].keys()})
        # Edge cubie touches 2 faces
        elif len(cubie_id) == 2:
            new_cubie = Edge(**{f:Square(cubies_dict[cubie_id][f]) for f in cubies_dict[cubie_id].keys()})
        # Center cubie touches only 1 face
        else:
            new_cubie = Centre(**{f:Square(cubies_dict[cubie_id][f]) for f in cubies_dict[cubie_id].keys()})
        cubies.add(new_cubie)

    return pc.Cube(cubies=cubies)


def is_correct(cube):
    """Returns True is a PyCube arg represents a complete cube, else False."""

    faces = ["F", "B", "D", "U", "L", "R"]
    complete = True
    # Check that each face has only 1 color (cube is solved)
    for face in faces:
        cols = cube.get_face(face)
        colors = [c for col in cols for c in col]
        if len(list(set(colors))) > 1:
            complete = False
            break
    return complete


def cube_to_config(cube):
    """Given a cube, return an init. config string = (URFDBL)*9*6."""

    # Get map from cube colors to cube faces
    colors_to_faces = get_map_colors_to_faces(cube)

    config_string = ""

    # Iterate over faces
    # Note: Face traversal order is URFDBL
    for face in FACES:
        face_array = cube.get_face(face)
        face_colors = [square.colour for col in face_array for square in col]
        face_chars = [colors_to_faces[color] for color in face_colors]
        for char in face_chars:
            config_string += char
    return config_string


def gen_init_config(length):
    """Generate a random initial configuration of a rubik's cube by randomly generating a formula of the specified length.
    
    Returns:
        Random initial cube configuration, as a string."""

    alg = pc.Formula().random(n=length)
    return str(alg)


def gen_response(cube):
    """Given acube, use the CFOPSolver in PyCuber to generate the corresponding response."""

    solver = CFOPSolver(cube)
    response = str(solver.solve(suppress_progress_messages=True).optimise())
    return response