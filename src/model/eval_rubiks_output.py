"""Given file with Rubik's output, test model performance."""

import argparse
import re
import pycuber as pc
from pycuber import Corner, Edge, Centre, Square
import random


parser = argparse.ArgumentParser()
parser.add_argument("--model_output", help="Path to file containing Rubik's data and corresponding model output.")
parser.add_argument("--prompt_start", help="Token indicating start of prompt (default <|startoftext|>[WP]).", default="<|startoftext|>[WP]")
parser.add_argument("--response_start", help="Token indicating start of response (default [RESPONSE]).", default="[RESPONSE]")
parser.add_argument("--response_end", help="Token indicating end of response (default <|endoftext|>).", default="<|endoftext|>")
args = parser.parse_args()

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
COLORS = ['red', 'blue', 'yellow', 'white', 'green', 'orange']


def get_map_colors_to_faces(cube):
    """Return a dict which maps color names to faces."""
    
    colors_to_faces = {}
    for color in COLORS:
        face = cube.which_face(color)
        colors_to_faces[color] = face
    return colors_to_faces


def get_map_faces_to_colors(cube):
    """Return a dict which maps faces to color names."""
    
    faces_to_colors = {}
    for color in COLORS:
        face = cube.which_face(color)
        faces_to_colors[face] = color
    return faces_to_colors


def config_to_cube(config):
    """Given a config string (6*9*(URFDBL)), produce a PyCuber.Cube object."""

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

def parse_line(line):
    """Parse a line in Rubik's data model output.
    
    Returns:
        A tuple containing initial configuration and generated formula.
    """

    match = re.match(f"{re.escape(args.prompt_start)}(.*){re.escape(args.response_start)}(.*){re.escape(args.response_end)}", line.strip())
    if match:
        prompt = match.group(1)
        response = match.group(2)
        return (prompt, response)
    else:
        return (None, None)


def eval_line(line):
    """Evaluates a single line of the output file.
    
    Returns:
        "Correct" if the generated response produces a solved cube from the intial configuration, "Incorrect" if it is valid but does not
        produce a solved cube, and "Invalid" if the response is an invalid formula or otherwise does not match the standard response format.
    """

    prompt, response = parse_line(line)
    if prompt and response:
        # Set initial cube config
        cube = config_to_cube(prompt)

        try:
            # Apply response formula
            cube(response)
        except ValueError as e:
            return "Invalid"
        # Check if cube is solved
        if is_correct(cube):
            return "Correct"
        else:
            return "Incorrect"
    else:
        return "Invalid"


def main():
    """Parse and evaluate model output on Rubik's data."""

    with open(args.model_output, 'r') as file:
        lines = [line for line in file.readlines()]

    # Sort responses into correct, incorrect, and invalid
    correct = []
    incorrect = []
    invalid = []
    for line in lines:
        result = eval_line(line)
        if result == "Correct":
            correct.append(line)
        elif result == "Incorrect":
            incorrect.append(line)
        else:
            invalid.append(line)

    # Print number and percentage of correct, incorrect, and invalid responses
    n_correct = len(correct)
    n_incorrect = len(incorrect)
    n_invalid = len(invalid)
    total = n_correct + n_incorrect + n_invalid
    r_correct = float(n_correct) / total
    r_incorrect = float(n_incorrect) / total
    r_invalid = float(n_invalid) / total

    print(f"Evaluating responses from {args.model_output}.")
    print(f"Correct: {n_correct}/{total} ~ {r_correct}")
    print(f"Incorrect: {n_incorrect}/{total} ~ {r_incorrect}")
    print(f"Invalid: {n_invalid}/{total} ~ {r_invalid}")


if __name__ == "__main__":
    main()

    

