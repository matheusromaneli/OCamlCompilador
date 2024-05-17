from collections import defaultdict
from .first_follow import Grammar

class LookAheadTable: 
    def __init__(self, grammar):
        self.grammar = grammar
        self.tabelaLookAhead = defaultdict(lambda: defaultdict(list))

    def createTable(self) :
        for non_terminal, productions in self.grammar.productions.items():
            for production in productions:
                first_group = self.calculate_first_group(production)
                for symbol in first_group:
                    if symbol != 'ε':
                        self.tabelaLookAhead[non_terminal][symbol] =  production
                if 'ε' in first_group:
                    follow_group = self.grammar.follow[non_terminal]
                    for symbol in follow_group:
                        self.tabelaLookAhead[non_terminal][symbol] = production

    def calculate_first_group(self, production):
        first_group = set()
        for symbol in production:
            if symbol in self.grammar.terminals:
                first_group.add(symbol)
                break
            elif symbol in self.grammar.non_terminals:
                first_group.update(self.grammar.first[symbol] - {''})
                if 'ε' not in self.grammar.first[symbol]:
                    break
            else:
                break
        else:
            first_group.add('')
        return first_group
    
    def display_lookahead_table(self):
        print("Lookahead Table:")
        for key in self.tabelaLookAhead:
            print(key,":")
            for symbol in self.tabelaLookAhead[key]:
                print(f"\t{symbol}: ")
                print("\t\t",self.tabelaLookAhead[key][symbol])
            
