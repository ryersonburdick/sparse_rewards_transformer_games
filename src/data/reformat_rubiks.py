"""
Process raw Rubik's data by adding start and end tokens. 
"""

# Open raw Rubik's data
with open("../../data/rubiks/raw/rubik.txt", 'r') as file:
    text = file.read()

PREFIX = "<|startoftext|>[WP] "
SEP = "[RESPONSE] "
SUFFIX = "<|endoftext|>"
output = ""
for line in text.split("\n"):
    halves = line.split("|")
    prompt, response = halves[0], halves[1]
    output += (PREFIX + prompt + SEP + response + SUFFIX + "\n")

with open("../../data/rubiks/processed/rubik.txt", 'w') as file:
    file.write(output)