from typing import List, Tuple
from scanner.automaton import Automaton, Rule, read_tokens

def process_file(file_name: str, automatons: List[Automaton]) -> List[str]:
    tokens = []
    with open(file_name, "r") as file:
        for line in file:
            word = line.strip()
            # Verifica se algum autômato aceita o token
            for automaton in automatons:
                matched_length = automaton.match(word)
                if matched_length == len(word):
                    tokens.append(word)
                    break  # Se um autômato aceitar o token, interrompe o loop
            else:
                print(f"Erro: A palavra '{word}' não corresponde ao padrão esperado.")
    return tokens