"""Visualize Rubik's cube solutions using cube.rider.biz."""

import wget
import argparse
from PIL import Image
import os
import sys

sys.path.insert(0, "src/utils")
from rubiks_utils import *

DEFAULT_CONFIG = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDBBBBBBBBBLLLLLLLLL"

parser = argparse.ArgumentParser()
parser.add_argument("--formula", help="String representation of rubik's formula from which to generate a gif. Individual steps should be separated by whitespace.")
parser.add_argument("--config", help="Initial configuration of cube that formula acts on (defaults to completed cube state).", default=DEFAULT_CONFIG)
parser.add_argument("--output", help="Name of file to write GIF to (default cube.gif).", default="cube.gif")
parser.add_argument("--duration", type=int, help="Desired GIF frame duration in ms (default 300).", default=300)
parser.add_argument("--repeat-last", help="Number of times to repeat last frame (default 0).", type=int, default=0)
args = parser.parse_args()


def get_cube_image(config, formula=None):
    """Given a cube configuration (9*6*URFDBL) and an optional formula, download an image of the cube after applying the formula.
    
    Returns name of the file where image is stored.
    """

    url = f"http://cube.rider.biz/visualcube.png?fmt=svg&size=350&pzl=3&fd={config.lower()}"
    if formula is not None:
        # Remove whitespace from formula
        formula = formula.replace(' ', '')
        url += f"&alg={formula}"
    image = wget.download(url)
    return image


def formula_to_gif(init_config, formula):
    """Given a Rubik's formula and initial cube configuration, create a gif of the cube as the formula is applied."""

    # Split formula into steps
    formula_steps = formula.split()

    # Store all GIF frames in order
    frames = []
    # Store filenames for frame images in order
    image_files = []

    # Get image for initial configuration
    start_frame = get_cube_image(init_config)
    image_files.append(start_frame)

    # Get images for subsequent configurations according to formula
    formula_string = ""
    for step in formula_steps:
        formula_string += step
        file = get_cube_image(init_config, formula=formula_string)
        image_files.append(file)

    # Use ordered list of image files to create gif and save
    for image_file in image_files:
        frames.append(Image.open(image_file))

    for i in range(args.repeat_last):
        frames.append(Image.open(image_files[-1]))

    frames[0].save(args.output, format='GIF', append_images=frames[1:], save_all=True, duration=args.duration, loop=0)

    # Delete all image files used to create gif
    for image_file in image_files:
        os.remove(image_file)


def main():
    formula_to_gif(args.config, args.formula)

if __name__ == "__main__":
    main()
