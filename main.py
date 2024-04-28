from scanner.automaton import create_automatons
from scanner.read_regex import read
from scanner.process_file import scan
from parser.first_follow import Grammar
from parser.look_ahead import LookAheadTable

tokens = read("files/regex.txt")
print(tokens)
automatons = create_automatons(tokens)

file_tokens = scan("files/file.txt", automatons)

grammar = Grammar()
grammar.read_grammar("files/ebnf.txt")  # Replace with actual path to the grammar file
grammar.calculate_first()
grammar.calculate_follow()
grammar.display_first_follow()

table_generator = LookAheadTable(grammar)
table_generator.createTable()
table_generator.display_lookahead_table()


print("Tokens:", file_tokens)
