from collections import defaultdict, deque

class Grammar:
    def __init__(self, grammar_file):
        self.productions = {}
        self.non_terminals = set()
        self.terminals = set()
        self.first = defaultdict(set)
        self.follow = defaultdict(set)
        self.start_symbol = "expr"


        self.read_grammar(grammar_file)
        self.identify_terminals()
        self.calculate_first()
        self.build_follow_set()

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

   
    def find_productions_with_non_terminal(self, non_terminal):
        productions_with_non_terminal = []
        for lhs, rhs_list in self.productions.items():
            for rhs in rhs_list:
                if non_terminal in rhs:
                    productions_with_non_terminal.append((lhs, rhs))
        return productions_with_non_terminal

    def build_follow_set(self):
        for nt in self.non_terminals:
            self.calculate_follow(nt)


    # def calculate_follow(self, symbol):
    #     if self.follow[symbol]:
    #         return self.follow[symbol]

    #     if not self.follow[symbol]:
    #         self.follow[symbol] = set()
    #         if symbol == self.start_symbol:
    #             self.follow[symbol].add('$') 

    #     list_productions = self.find_productions_with_non_terminal(symbol)

    #     for lhs, rhs in list_productions:
    #         symbol_index = rhs.index(symbol)
    #         follow_index = symbol_index + 1

    #         while True:
    #             if follow_index >= len(rhs):
    #                 if lhs != symbol:
    #                     self.follow[symbol].update(self.calculate_follow(lhs))
    #                 break

    #             follow_symbol = rhs[follow_index]
    #             self.follow[symbol].update(self.first[follow_symbol] - {'epsilon'})

    #             if 'epsilon' not in self.first[follow_symbol]:
    #                 break

    #             follow_index += 1

    #     return self.follow[symbol]

    def calculate_follow(self, symbol):
        # If the follow set for the symbol has already been calculated, return it.
        if symbol in self.follow:
            return self.follow[symbol]

        # Initialize the follow set for the symbol if it hasn't been initialized.
        self.follow[symbol] = set()
        if symbol == self.start_symbol:
            self.follow[symbol].add('$')  # Start symbol always contains '$' in its follow set.

        # Find all productions where the symbol appears on the RHS.
        list_productions = self.find_productions_with_non_terminal(symbol)
        for lhs, rhs in list_productions:
            symbol_index = rhs.index(symbol)
            follow_index = symbol_index + 1

            while True:
                if follow_index == len(rhs):  # Check if it's the end of the production.
                    if lhs != symbol:  # To avoid cases like B -> aB which can lead to infinite recursion.
                        self.follow[symbol].update(self.calculate_follow(lhs))
                    break

                follow_symbol = rhs[follow_index]
                first_of_follow_symbol = self.first[follow_symbol]

                # Exclude epsilon if it exists in the first set.
                follow_without_epsilon = {x for x in first_of_follow_symbol if x != 'epsilon'}

                # Merge the first set of the follow symbol, except for epsilon.
                self.follow[symbol].update(follow_without_epsilon)

                # If there is no epsilon in the first set, stop.
                if 'epsilon' not in first_of_follow_symbol:
                    break

                follow_index += 1

        return self.follow[symbol]


       




# TESTANDO
grammar = Grammar("files\\ebnf.txt")

# print("Non-Terminals:", grammar.non_terminals)
# print("Terminals:", grammar.terminals)

print("Productions:")
for lhs, rhs in grammar.productions.items():
    print(lhs, "->", rhs)

# print("First Sets:")
# for nt, f in grammar.first.items():
#     if f.__len__() > 0:
#         print(f"FIRST({nt}) = {f}")

teste = grammar.find_productions_with_non_terminal( "expr")
print(teste)

# print("Follow Sets:")
# for nt, f in grammar.follow.items():
#     if f.__len__() > 0:
#         print(f"FOLLOW({nt}) = {f}")

