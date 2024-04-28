import re
from collections import defaultdict

class Grammar:
    def __init__(self):
        self.productions = defaultdict(list)
        self.first = defaultdict(set)
        self.follow = defaultdict(set)
        self.terminals = set()
        self.non_terminals = set()

    def add_production(self, non_terminal, production):
        self.productions[non_terminal].append(production)
        self.non_terminals.add(non_terminal)
        for symbol in production:
            if symbol.islower() or re.match(r'[+"*|()[\]{}]', symbol):
                self.terminals.add(symbol)
            else:
                self.non_terminals.add(symbol)

    def calculate_first(self):
        changed = True
        while changed:
            changed = False
            for non_terminal in self.productions:
                for production in self.productions[non_terminal]:
                    before_change = len(self.first[non_terminal])
                    if not production:
                        self.first[non_terminal].add("ε")
                    else:
                        for symbol in production:
                            if symbol in self.terminals:
                                self.first[non_terminal].add(symbol)
                                break
                            else:
                                self.first[non_terminal].update(self.first[symbol] - {'ε'})
                                if 'ε' not in self.first[symbol]:
                                    break
                            # If ε is in all symbols of the production
                        else:
                            self.first[non_terminal].add('ε')
                    if len(self.first[non_terminal]) > before_change:
                        changed = True

    def calculate_follow(self):
        self.follow[next(iter(self.productions))].add('$')  # Start symbol
        changed = True
        while changed:
            changed = False
            for non_terminal in self.productions:
                for production in self.productions[non_terminal]:
                    follow_temp = self.follow[non_terminal]
                    for symbol in reversed(production):
                        if symbol in self.non_terminals:
                            before_change = len(self.follow[symbol])
                            self.follow[symbol].update(follow_temp)
                            if 'ε' in self.first[symbol]:
                                follow_temp = follow_temp.union(self.first[symbol] - {'ε'})
                            else:
                                follow_temp = self.first[symbol]
                            if len(self.follow[symbol]) > before_change:
                                changed = True
                        else:
                            follow_temp = self.first[symbol]

    def read_grammar(self, file_path):
        with open(file_path, 'r') as file:
            data = file.read()
        rules = data.split('\n')
        for rule in rules:
            if "::=" in rule:
                non_terminal, productions = rule.split('::=')
                non_terminal = non_terminal.strip()
                productions = [p.strip().split() for p in productions.split('|')]
                for production in productions:
                    self.add_production(non_terminal, production)

    def display_first_follow(self):
        print("First Sets:")
        for non_terminal in sorted(self.first):
            print(f"{non_terminal}: {self.first[non_terminal]}")
        print("\nFollow Sets:")
        for non_terminal in sorted(self.follow):
            print(f"{non_terminal}: {self.follow[non_terminal]}")

# Usage
if __name__ == "__main__":
    grammar = Grammar()
    grammar.read_grammar("files/ebnf.txt")  # Replace with actual path to the grammar file
    grammar.calculate_first()
    grammar.calculate_follow()
    grammar.display_first_follow()
