from scanner.automaton import create_automatons
from scanner.read_regex import read
from scanner.process_file import scan
from parser.first_follow import Grammar
from parser.look_ahead import LookAheadTable
from parser.process_file import parser

tokens = read("files/regex.txt")
# print(tokens)
automatons = create_automatons(tokens)

file_tokens = scan("files/file.txt", automatons)

grammar = Grammar("files/ebnf.txt")

table_generator = LookAheadTable(grammar)
table_generator.display_lookahead_table()
print("Starting parser...")

semantic_errors = parser(file_tokens, ["expr"], table_generator.lookahead_table)

print("Success: ", semantic_errors)