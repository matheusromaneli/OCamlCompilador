from collections import defaultdict
from parser.first_follow import Grammar

class LookAheadTable:
    def __init__(self, grammar):
        self.grammar = grammar
        self.lookahead_table = self.build_lookahead_table()

    def build_lookahead_table(self):
        lookahead_table = defaultdict(dict)
        for non_terminal, productions in self.grammar.productions.items():
            for production in productions:
                lookaheads = set()
                for symbol in production:
                    lookaheads.update(self.grammar.first[symbol] - {'epsilon'})
                    if 'epsilon' not in self.grammar.first[symbol]:
                        break
                else:
                    lookaheads.update(self.grammar.follow[non_terminal])
                for lookahead in lookaheads:
                    lookahead_table[non_terminal][lookahead] = production
        return lookahead_table


    def display_lookahead_table(self):
        for non_terminal, lookaheads in self.lookahead_table.items():
            for lookahead, production in lookaheads.items():
                print(f"Lookahead[{non_terminal}][{lookahead}] = {production}")

# TESTE
# grammar_file_path = 'C:\\Users\\dario\\OneDrive\\Desktop\\uff\\CompiladoresFinal\\OCamlCompilador\\files\\ebnf.txt'
# grammar = Grammar(grammar_file_path)
# lookahead_table = LookAheadTable(grammar)
# lookahead_table.display_lookahead_table()
