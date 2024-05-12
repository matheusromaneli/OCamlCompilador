from typing import List
from scanner.automaton import Automaton, Token

def scan(file_name: str, automatons: List[Automaton]) -> List[Token]:
    tokens = []
    with open(file_name, "rb") as file:
        while file.read(1) != b'':
            file.seek(-1, 1)
            curr_input = file.read(1)
            while curr_input == b' ':
                curr_input = file.read(1)
            file.seek(-1, 1)

            biggest: Token | None = None
            curr = file.tell()
            for automaton in automatons:
                file.seek(curr)
                token = automaton.match(file)
                if (biggest is None or token.size > biggest.size) and token.size > 0:
                    biggest = token
            if biggest is not None:
                tokens.append(biggest)
                curr = file.seek(biggest.end)
            else:
                print("Could not process:", curr_input)
    return tokens