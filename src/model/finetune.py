"""Download or load a GPT-2 instance and fine-tune on specified text data file."""

import gpt_2_simple as gpt2
import os
import tensorflow as tf
import argparse

# Set default model size
DEFAULT_MODEL_NAME = "124M"
# Paths to model and checkpoint locations
MODEL_DIR = "../../models"
CHECKPOINT_DIR = "../../checkpoint"

parser = argparse.ArgumentParser(description="Download or load GPT-2 instance and fine-tune on text data.")
parser.add_argument("--model_name", help=f"Size of GPT-2 insance to download from gpt-2-simple (default '{DEFAULT_MODEL_NAME}').", 
    default=DEFAULT_MODEL_NAME, required=False)
parser.add_argument("--run", help="Path to run folder for existing model.", default=None, required=False)
parser.add_argument("--data", help="Path to text data file to use for fine-tuning.", required=True)

args = parser.parse_args()

def main():
    # Clear tensorflow graph
    tf.reset_default_graph()

    # Start gpt-2 sess
    sess = gpt2.start_tf_sess()

    # Load existing model if specified
    if args.run is not None:
        print(f"Loading run {args.run}...")
        gpt2.load_gpt2(sess, run_name=args.run, model_name=args.model_name, model_dir=MODEL_DIR, checkpoint_dir=CHECKPOINT_DIR)
    # Otherwise download new model
    else:
        gpt2.download_gpt2(model_dir=MODEL_DIR, model_name=args.model_name)

    # Fine-tune model on data file
    gpt2.finetune(sess,
        args.data,
        model_name=args.model_name,
        model_dir=MODEL_DIR,
        checkpoint_dir=CHECKPOINT_DIR,
        run_name=args.run)


if __name__ == "__main__":
    main()