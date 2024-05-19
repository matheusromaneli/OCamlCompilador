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


    def calculate_follow(self, symbol):
    # Se o conjunto de follow já foi calculado, retorna-o diretamente
        if self.follow[symbol]:
            return self.follow[symbol]

        # Inicializa o conjunto de follow para o símbolo, se ainda não inicializado
        if not self.follow[symbol]:
            self.follow[symbol] = set()
            if symbol == self.start_symbol:
                self.follow[symbol].add('$')  # Adiciona o símbolo de fim de entrada para o símbolo inicial

        # Encontra todas as produções que usam o símbolo
        list_productions = self.find_productions_with_non_terminal(symbol)

        for lhs, rhs in list_productions:
            symbol_index = rhs.index(symbol)
            follow_index = symbol_index + 1

            while True:
                if follow_index >= len(rhs):
                    # Se o símbolo está no final do RHS, pegue o follow do LHS (exceto se LHS == símbolo para evitar loop infinito)
                    if lhs != symbol:
                        self.follow[symbol].update(self.calculate_follow(lhs))
                    break

                follow_symbol = rhs[follow_index]
                # Adiciona todos os primeiros do símbolo seguinte no RHS ao follow do símbolo atual
                self.follow[symbol].update(self.first[follow_symbol] - {'epsilon'})

                # Se o primeiro do próximo símbolo não contém epsilon, pare aqui
                if 'epsilon' not in self.first[follow_symbol]:
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

