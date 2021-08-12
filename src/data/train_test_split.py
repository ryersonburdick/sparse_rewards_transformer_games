"""Split text file into train and test datasets."""

import os
import argparse
import random
from math import floor

parser = argparse.ArgumentParser()
parser.add_argument("--data", help="Path to dataset text file.", required=True)
parser.add_argument("--train", type=float, default=0.8, help="Proportion of samples (lines) to use in training dataset.", required=False)
parser.add_argument("--test", type=float, default=None, help="Proportion of samples (lines) to use in test dataset. If not specified, defaults to 1.0 - train proportion.", required=False)
parser.add_argument("--train_path", default=None, help="Path to text file where train samples will be stored. Defaults to data/../processed/train.txt")
parser.add_argument("--test_path", default=None, help="Path to text file where test samples will be stored. Defaults to data/../processed/test.txt")

args = parser.parse_args()

def main():
    # Read data file
    with open(args.data, 'r') as file:
        samples = [line for line in file.readlines()]
    
    split_indx = floor(len(samples) * args.train)
    # Shuffle data and split
    random.shuffle(samples)
    train_samples = samples[:split_indx]
    test_samples = samples[split_indx:]

    # Write train data
    with open(args.train, 'w') as file:
        file.write("\n".join(train_samples))
    
    # Write test data
    with open(args.test, 'w') as file:
        file.write("\n".join(test_samples))


if __name__ == "__main__":
    main()
