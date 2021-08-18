from pycuber.solver import CFOPSolver
import pycuber as pc
import random
import argparse
from math import ceil
import sys

sys.path.insert(0, "src/utils")
from rubiks_utils import *


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
            prompt = cube_to_config(cube)
            response = gen_response(cube)
            sample = f"{args.prompt_start}{prompt}{args.response_start}{response}{args.response_end}"
            gen_samples.append(sample)

    # Write generated samples to output file
    with open(args.output, 'w') as file:
        file.write("\n".join(gen_samples))


if __name__ == "__main__":
    main()