"""
Clean a text file of Rubik's cube solutions data by removing all scramble-solution pairs
which do not resolve to a completed cube.
"""

import pycuber as pc
import argparse

parser = argparse.ArgumentParser(description="Clean text Rubik's solution data.")
parser.add_argument('--input', type=str, help="Path to input data file.")
parser.add_argument('--output', type=str, help="Name of output file to write cleaned data to (default rubiks_clean.txt).", 
  default="rubiks_clean.txt", required=False)
parser.add_argument('--delim', type=str, help="Delimiter string used to separate prompt (cube scramble formula) from response (cube solution formula) (default '|').", 
  default="|", required=False)
args = parser.parse_args()


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


def main():
  # Load input file specified by command line arg
  with open(args.input, 'r') as file:
    data = file.read()
  
  output = []
  # Iterate through each line and append correct lines to output
  for line in data.split("\n"):
    split_line = line.split(args.delim)
    prompt, response = split_line[0], split_line[1]

    # Create a new cube
    cube = pc.Cube()
    # Apply prompt formula
    cube(prompt)
    # Apply response formula
    cube(response)
    # Ensure resulting cube is correct (i.e., response is correct formula for solving scramble specified by prompt)
    if is_correct(cube):
      output.append(line)
    
  # Join output lines with newline and print to output file
  output_str = "\n".join(output)
  with open(args.output, 'w') as file:
    file.write(output_str)

if __name__ == "__main__":
  main()
