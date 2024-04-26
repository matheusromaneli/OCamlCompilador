from scanner.automaton import read_tokens
from scanner.read_regex import read
from scanner.process_file import process_file

tokens = read("regex.txt")
print(tokens)
automatons = read_tokens(tokens)

file_tokens = process_file("file.txt", automatons)

print("Tokens:", file_tokens)
