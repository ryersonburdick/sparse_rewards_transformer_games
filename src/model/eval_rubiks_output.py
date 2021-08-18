"""Given file with Rubik's output, test model performance."""

import argparse
import re
import pycuber as pc
from pycuber import Corner, Edge, Centre, Square
from pycuber.solver import CFOPSolver
import random
import sys

sys.path.insert(0, "src/utils")
from rubiks_utils import *


parser = argparse.ArgumentParser()
parser.add_argument("--model_output", help="Path to file containing Rubik's data and corresponding model output.")
parser.add_argument("--prompt_start", help="Token indicating start of prompt (default <|startoftext|>[WP]).", default="<|startoftext|>[WP]")
parser.add_argument("--response_start", help="Token indicating start of response (default [RESPONSE]).", default="[RESPONSE]")
parser.add_argument("--response_end", help="Token indicating end of response (default <|endoftext|>).", default="<|endoftext|>")
args = parser.parse_args()


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
