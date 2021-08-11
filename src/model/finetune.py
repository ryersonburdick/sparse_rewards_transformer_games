"""Download or load a GPT-2 instance and fine-tune on specified text data file."""

import gpt_2_simple as gpt2
import os
import tensorflow as tf
import argparse

# Set default model size
DEFAULT_MODEL_NAME = "124M"
# Paths to model and checkpoint locations
MODEL_DIR = "models"
CHECKPOINT_DIR = "checkpoint"

parser = argparse.ArgumentParser(description="Download or load GPT-2 instance and fine-tune on text data.")
parser.add_argument("--model_name", help=f"Size of GPT-2 insance to download from gpt-2-simple (default '{DEFAULT_MODEL_NAME}').", 
    default=DEFAULT_MODEL_NAME, required=False)
parser.add_argument("--run", help="Path to run folder for existing model.", default=None, required=False)
parser.add_argument("--data", help="Path to text data file to use for fine-tuning.", required=True)
# Hyperparameters
parser.add_argument("--batch_size", type=int, default=1)
parser.add_argument("--lr", type=float, default=0.0001)
parser.add_argument("--sample_every", type=int, default=100)
parser.add_argument("--sample_len", type=int, default=1023)
parser.add_argument("--print_every", type=int, default=1)
parser.add_argument("--save_every", type=int, default=500)
parser.add_argument("--optimizer", default="adam")
parser.add_argument("--overwrite", type=bool, default=False)

args = parser.parse_args()

def main():

    # Start gpt-2 sess
    sess = gpt2.start_tf_sess()

    # Load existing model if specified
    if args.run is not None:
        print(f"Loading model {args.run}...")
        gpt2.load_gpt2(sess, run_name=args.run, model_dir=MODEL_DIR, checkpoint_dir=CHECKPOINT_DIR)
    # Otherwise download new model
    else:
        print(f"Downloading model {args.model_name}...")
        gpt2.download_gpt2(model_dir=MODEL_DIR, model_name=args.model_name)

    # Fine-tune model on data file
    gpt2.finetune(sess,
        args.data,
        model_name=args.model_name,
        model_dir=MODEL_DIR,
        checkpoint_dir=CHECKPOINT_DIR,
        batch_size=args.batch_size,
        learning_rate=args.lr,
        sample_every=args.sample_every,
        sample_length=args.sample_len,
        save_every=args.save_every,
        print_every=args.print_every,
        optimizer=args.optimizer,
        overwrite=args.overwrite)


if __name__ == "__main__":
    main()
