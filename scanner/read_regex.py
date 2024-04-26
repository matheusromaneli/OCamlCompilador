# Matheus -> "M", "a", ... == [A-z]
# "M" == [A-z] -> True

from typing import Optional


ANY_CHAR = "A-z"
ANY_NUMBER = "0-9"
class Rule:

    def __init__(self, expression: str, repeatable: bool = False) -> None:
        self.expression = expression #A-z
        self.repeatable = repeatable #True

    def __eq__(self, __value: str) -> bool:
        if ANY_CHAR in self.expression and __value.isalpha():
            return True
        if ANY_NUMBER in self.expression and __value.isnumeric():
            return True
        if self.expression == __value:
            return True
        return False

    def __str__(self):
        return f"{self.expression}{'(repeatable)' if self.repeatable else ''}"
    
    def __repr__(self) -> str:
        return self.__str__()

def parse_regex(regex:str):
    start = None
    end = None
    parsed = []
    for index in range(len(regex)):
        if regex[index] == '[':
            start = index
        if start is not None and regex[index] == ']':
            end = index
        if start is not None and end is not None:
            parsed.append(regex[start+1:end])
            start = None
            end = None
        elif start is None and end is None:
            parsed.append(regex[index])
    return parsed
        
def read_rules(expressions: list[str]):
    rules = []
    for index in range(len(expressions)):
        if expressions[index] != '*':
            expression = expressions[index]
            repeatable = False
            if index + 1 < len(expressions):
                repeatable = expressions[index+1] == '*'                
            rules.append(Rule(expression, repeatable))
    return rules


def read(file_name):
    tokens = {}
    with open(file_name, "r") as file:
        for line in file:
            token, regex = line.split(":", 1)

            token = token.strip()  
            regex = regex.strip()
            parsed_regex = parse_regex(regex)

            rules = read_rules(parsed_regex)
            tokens[token] = rules
    return tokens
