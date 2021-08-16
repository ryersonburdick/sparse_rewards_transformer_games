from pycuber.solver import CFOPSolver
import pycuber as pc
import random
import argparse
from math import ceil


parser = argparse.ArgumentParser()
parser.add_argument("--n_samples", type=int, help="Number of samples to generate (default 10000).", default=10000)
parser.add_argument("--min_length", type=int, 
    help="Minimum length (in face turns) of intial cube configurations. Note that lengths of generated samples will be uniformly \
        distributed from --min_length to --max_length. Default is 1.", default=1)
parser.add_argument("--max_length", type=int,
    help="Maximum length (in face turns) of intial cube configurations. Note that lengths of generated samples will be uniformly \
        distributed from --min_length to --max_length. Default is 10.", default=10)
parser.add_argument("--output", help="Name of output file to write generated samples to. Default rubiks_generated.txt.", default="rubiks_generated.txt")
parser.add_argument("--prompt_start", help="Token indicating start of prompt (default <|startoftext|>[WP]).", default="<|startoftext|>[WP]")
parser.add_argument("--response_start", help="Token indicating start of response (default [RESPONSE]).", default="[RESPONSE]")
parser.add_argument("--response_end", help="Token indicating end of response (default <|endoftext|>).", default="<|endoftext|>")
args = parser.parse_args()

COLORS = ['red', 'blue', 'yellow', 'white', 'green', 'orange']
FACES = ["U", "R", "F", "D", "B", "L"]

def get_map_colors_to_faces(cube):
    """Return a dict which maps color names to faces."""
    
    colors_to_faces = {}
    for color in COLORS:
        face = cube.which_face(color)
        colors_to_faces[color] = face
    return colors_to_faces


def get_config_string(cube):
    """Given a cube, return a init. config string = (URFDBL)*9."""

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


def main():
    """Generate Rubik's prompt-response pairs."""

    # Config lengths are uniformly distributed by default from min_length to max_length
    # Determine how many samples are required of each length
    n_lengths = args.max_length - (args.min_length - 1)
    samples_per_len = ceil(args.n_samples / n_lengths)

    # Store generated samples
    gen_samples = []

    # Generate appropriate amount of samples for each sample length
    for length in range(args.min_length, args.max_length+1):
        for _ in range(samples_per_len):
            config = gen_init_config(length)
            cube = pc.Cube()
            cube(config)
            prompt = get_config_string(cube)
            response = gen_response(cube)
            sample = f"{args.prompt_start}{prompt}{args.response_start}{response}{args.response_end}"
            gen_samples.append(sample)

    # Write generated samples to output file
    with open(args.output, 'w') as file:
        file.write("\n".join(gen_samples))


if __name__ == "__main__":
    main()