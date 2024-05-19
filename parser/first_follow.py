from collections import defaultdict

class Grammar:
    def __init__(self, grammar_file):
        self.productions = {}
        self.non_terminals = set()
        self.terminals = set()
        self.first = defaultdict(set)
        self.follow = defaultdict(set)

        self.read_grammar(grammar_file)
        self.identify_terminals()
        self.calculate_first()
        self.calculate_follow()

    def read_grammar(self, grammar_file):
        with open(grammar_file, 'r', encoding="utf-8") as file:
            for line in file:
                if "::=" in line:
                    lhs, rhs = line.split("::=")
                    lhs = lhs.strip()

                    rhs = rhs.strip().split("|")
                    aux_rhx = []
                    for alt in rhs:
                        aux_rhx.append(alt.strip().split())

                    self.productions[lhs] = aux_rhx
                    self.non_terminals.add(lhs)

    def identify_terminals(self):
        all_symbols = set()
        for rhs in self.productions.values():
            for element in rhs:
                all_symbols.update(element)
        self.terminals = all_symbols - self.non_terminals

    def calculate_first(self):
        def first_of(symbol):
            if symbol in self.terminals:
                return {symbol}
            if symbol in computed:
                return self.first[symbol]
            computed.add(symbol)
            result = set()
            for production in self.productions[symbol]:
                if len(production) > 0:
                    sym_first = first_of(production[0])
                    result.update(sym_first - {'epsilon'})
                    
                else:
                    result.add('epsilon')
            self.first[symbol].update(result)
            return result

        computed = set()
        for non_terminal in self.non_terminals:
            first_of(non_terminal)

    def calculate_follow(self):
        # Start symbol (assuming the first non-terminal in the list is the start symbol)
        start_symbol = next(iter(self.non_terminals))
        self.follow[start_symbol].add('$')  # End of input symbol

        while True:
            updated = False
            for lhs in self.productions:
                for production in self.productions[lhs]:
                    follow_temp = self.follow[lhs].copy()
                    for symbol in reversed(production):
                        if symbol in self.non_terminals:
                            if self.follow[symbol].update(follow_temp):
                                updated = True
                            if 'epsilon' in self.first[symbol]:
                                follow_temp.update(self.first[symbol] - {'epsilon'})
                            else:
                                follow_temp = self.first[symbol].copy()
                        else:
                            follow_temp = self.first[symbol].copy()
            if not updated:
                break

# TESTANDO
grammar = Grammar('files\\ebnf.txt')

# print("Non-Terminals:", grammar.non_terminals)
# print("Terminals:", grammar.terminals)

# print("Productions:")
# for lhs, rhs in grammar.productions.items():
#     print(lhs, "->", rhs)

print("First Sets:")
for nt, f in grammar.first.items():
    if f.__len__() > 0:
        print(f"FIRST({nt}) = {f}")


print("Follow Sets:")
for nt, f in grammar.follow.items():
    if f.__len__() > 0:
        print(f"FOLLOW({nt}) = {f}")

