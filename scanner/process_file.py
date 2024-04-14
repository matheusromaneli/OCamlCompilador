import os
from typing import List
from scanner.automaton import Automaton, Token

def process_file(file_name: str, automatons: List[Automaton]) -> List[str]:
    tokens = []
    with open(file_name, "rb") as file:
        while file.read(1) != b'':
            file.seek(-1, 1)
            while file.read(1) == b' ':
                pass
            file.seek(-1, 1)

            biggest: Token | None = None
            curr = file.tell()
            for automaton in automatons:
                file.seek(curr)
                token = automaton.match(file)
                if biggest is None or token.size > biggest.size:
                    biggest = token
            tokens.append(biggest)
            if biggest is not None:
                curr = file.seek(biggest.end)
    return tokens