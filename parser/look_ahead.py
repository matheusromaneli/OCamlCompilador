from parser.first_follow import Grammar

class LookAheadTable: 
    def __init__(self, grammar):
        self.grammar = grammar
        self.tabelaLookAhead = {}

    def createTable(self) :
        for non_terminal, productions in self.grammar.productions.items():
            for production in productions:
                first_group = self.calculate_first_group(production)
                for symbol in first_group:
                    if symbol != 'ε':
                        self.tabelaLookAhead[(non_terminal, symbol)] =  production
                if 'ε' in first_group:
                    follow_group = self.grammar.follow[non_terminal]
                    for symbol in follow_group:
                        self.tabelaLookAhead[(non_terminal, symbol)] = production

    def calculate_first_group(self, production):
        first_group = set()
        for symbol in production:
            if symbol in self.grammar.terminals:
                first_group.add(symbol)
                break
            elif symbol in self.grammar.non_terminals:
                first_group.update(self.grammar.first[symbol] - {'ε'})
                if 'ε' not in self.grammar.first[symbol]:
                    break
            else:
                break
        else:
            first_group.add('ε')
        return first_group
    
    def display_lookahead_table(self):
        print("Lookahead Table:")
        for key, production in self.tabelaLookAhead.items():
            non_terminal, symbol = key
            print(f"{non_terminal} -> {production} when lookahead is {symbol}")
            

if __name__ == "__main__":              
    grammar = Grammar()
    grammar.read_grammar("files/ebnf.txt")  # Substitua 'ebnf.txt' pelo caminho do seu arquivo com a gramática
    grammar.calculate_first()
    grammar.calculate_follow()

    table_generator = LookAheadTable(grammar)
    table_generator.createTable()
    table_generator.display_lookahead_table()