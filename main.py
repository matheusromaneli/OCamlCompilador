from scanner.automaton import read_tokens
from scanner.read_regex import read

tokens = read("regex.txt")
automatons = read_tokens(tokens)
