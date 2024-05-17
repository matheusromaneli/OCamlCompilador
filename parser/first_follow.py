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
                    rhs = [option.strip().split() for option in rhs.split("|")]
                    self.productions[lhs] = rhs
                    self.non_terminals.add(lhs)

    def identify_terminals(self):
        all_symbols = set()
        for rhs in self.productions.values():
            for option in rhs:
                all_symbols.update(option)
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
                for sym in production:
                    sym_first = first_of(sym)
                    result.update(sym_first - {''})
                    if '' not in sym_first:
                        break
                else:
                    result.add('')
            self.first[symbol] = result
            return result

        computed = set()
        for non_terminal in self.non_terminals:
            first_of(non_terminal)

    def calculate_follow(self):
        for non_terminal in self.non_terminals:
            self.follow[non_terminal] = set()
        self.follow[next(iter(self.non_terminals))].add('$')  # Assume first non-terminal as start

        changed = True
        while changed:
            changed = False
            for lhs, productions in self.productions.items():
                for production in productions:
                    for i, symbol in enumerate(production):
                        if symbol in self.non_terminals:
                            next_first = set()
                            for j in range(i + 1, len(production)):
                                next_first.update(self.first[production[j]] - {''})
                                if '' not in self.first[production[j]]:
                                    break
                            else:
                                next_first.update(self.follow[lhs])

                            before_update = len(self.follow[symbol])
                            self.follow[symbol].update(next_first)
                            if before_update != len(self.follow[symbol]):
                                changed = True
                            if i == len(production) - 1 or '' in self.first[production[i + 1]]:
                                before_update = len(self.follow[symbol])
                                self.follow[symbol].update(self.follow[lhs])
                                if before_update != len(self.follow[symbol]):
                                    changed = True

# Exemplo de uso
grammar = Grammar('C:\\Users\\engcl\\OneDrive\\Documentos\\UFF\\Compiladores\\OCamlCompilador\\files\\ebnf.txt')
print("Non-Terminals:", grammar.non_terminals)
print("Terminals:", grammar.terminals)
print("Productions:")
for lhs, rhs in grammar.productions.items():
    print(lhs, "->", rhs)
print("First Sets:")
for nt, f in grammar.first.items():
    print(f"FIRST({nt}) = {f}")
print("Follow Sets:")
for nt, f in grammar.follow.items():
    print(f"FOLLOW({nt}) = {f}")

