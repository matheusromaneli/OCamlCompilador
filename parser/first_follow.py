class Grammar:
    def __init__(self, grammar_file):
        self.productions = {}
        self.non_terminals = set()
        self.terminals = set()

        self.read_grammar(grammar_file)
        self.identify_terminals()

    def read_grammar(self, grammar_file):
        with open(grammar_file, 'r', encoding="utf-8") as file:
            for line in file:
                if "::=" in line:
                    lhs, rhs = line.split("::=")
                    lhs = lhs.strip()
                    rhs = rhs.strip().split("|")

                    self.productions[lhs] = rhs
                    self.non_terminals.add(lhs)

    def identify_terminals(self):
        for rhs in self.productions.values():
            for alternative in rhs:
                for symbol in alternative:
                    if symbol not in self.non_terminals:
                        self.terminals.add(symbol)

    def calculate_first(self):
        for non_terminal in self.non_terminals:
            self.first[non_terminal] = set()

       


# Exemplo de uso
grammar = Grammar('C:\\Users\\dario\\OneDrive\\Desktop\\uff\\CompiladoresFinal\\OCamlCompilador\\files\\ebnf.txt')
# print("Non-Terminals:", grammar.non_terminals)
# print("Terminals:", grammar.terminals)
print("Productions:")
for lhs, rhs in grammar.productions.items():
    print(lhs, "->", rhs)
