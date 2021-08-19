"""Given a run name and a prefix or a text file of prefix-response pairs, use the prefix to generate responses."""

import gpt_2_simple as gpt2
import tensorflow as tf
import os
import argparse

# Paths to model and checkpoint locations
MODEL_DIR = "models"
CHECKPOINT_DIR = "checkpoint"
# Special tokens indicating start of prompt, start of response, and end of response
PROMPT_START_TOKEN = "<|startoftext|>[WP]"
RESPONSE_START_TOKEN = "[RESPONSE]"
END_TOKEN = "<|endoftext|>"

parser = argparse.ArgumentParser()
parser.add_argument("--run_name", help="Name of existing model run to load and use for generation.", required=True)
parser.add_argument("--prefix", default=None, 
    help="Text prefix to use for generation. If specified, ignores --data argument and prints the generated response to this prefix before quitting.", required=False)
parser.add_argument("--data", default=None, 
    help="File containing lines in the format <|startoftext|>[WP] (prefix)[RESPONSE](response)<|endoftext|> whose prefixes will be used to generate responses.", required=False)
parser.add_argument("--output", default=None, help="Name of file to write generated response(s) to. Default is {run_name}_responses.txt", required=False)
parser.add_argument("--temperature", type=float, default=0.7)
parser.add_argument("--n_samples", type=int, default=1)
parser.add_argument("--stop_after", type=int, default=None)
parser.add_argument("--verbose", type=bool, default=False)
parser.add_argument("--save_every", type=int, default=25)
args = parser.parse_args()


def main():
    # Start session
    sess = gpt2.start_tf_sess()

    # Load pre-trained/tuned model
    gpt2.load_gpt2(sess, run_name=args.run_name, checkpoint_dir=CHECKPOINT_DIR)

    # If prefix is specified, print generated response
    if args.prefix is not None:
        output = gpt2.generate(
            sess, 
            run_name=args.run_name, 
            checkpoint_dir=CHECKPOINT_DIR, 
            prefix=args.prefix, 
            nsamples=args.n_samples, 
            temperature=args.temperature, 
            return_as_list=True)[0]
        print(output)

        # Write output to file, if specified
        if args.output is not None:
            with open(args.output, 'w') as file:
                file.write(args.prefix + output)

    # Otherwise, load data file, separate prefixes from responses, generate output for each prefix, and record
    else:
        # Open data file
        with open(args.data, 'r') as file:
            samples = [line for line in file.readlines()]
        
        # Split each sample into prompt and existing (correct) response
        split_samples = [sample.split(RESPONSE_START_TOKEN) for sample in samples]
        prompts = [sample[0] + RESPONSE_START_TOKEN for sample in split_samples]

        # Generate a new response for each prompt, truncate at the end-of-line token
        def truncate_response(response):
            return response.split(END_TOKEN)[0] + END_TOKEN
            
        output = []
        n_prompts = len(prompts)

        if args.stop_after is None:
            args.stop_after = n_prompts

        # If output file not specified, default to {run_name}_responses.txt
        if args.output is None:
            output_file = args.run_name + "_responses.txt"
        else:
            output_file = args.output

        try:
            for i, prompt in enumerate(prompts):
                if i >= args.stop_after:
                    break
                gen = gpt2.generate(
                        sess, 
                        run_name=args.run_name, 
                        checkpoint_dir=CHECKPOINT_DIR, 
                        prefix=prompt, 
                        nsamples=args.n_samples,
                        temperature=args.temperature,
                        return_as_list=True
                    )[0]
                # Truncate
                gen = truncate_response(gen)

                # Show progress if applicable
                if args.verbose:
                    print(f"[{i+1} / {args.stop_after}] {gen}")

                output.append(gen)

                # Save intermittently
                if (i + 1) % args.save_every == 0:
                    if args.verbose:
                        print(f"Saving to {output_file}...")
                    with open(output_file, 'w') as file:
                        file.write("\n".join(output))

        except KeyboardInterrupt as e:
            pass
        
        if args.verbose:
            print(f"Saving to {output_file}...")
        with open(output_file, 'w') as file:
            file.write("\n".join(output))


if __name__ == "__main__":
    main()