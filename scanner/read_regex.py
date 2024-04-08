# Matheus -> "M", "a", ... == [A-z]
# "M" == [A-z] -> True

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

#[A-z][A-z|0-9]*

def regex_to_rule(regex: str) -> Rule:
    if regex.startswith("["):
        if regex[-1] == "*":
            return Rule(regex[1:-2], repeatable=True)
        return Rule(regex[1:-1])
    #['let'] -> ['l','e','t']
    return [Rule(ex) for ex in regex] #let

def read(file_name):
    tokens = {}
    with open("regex.txt", "r") as file:
        for line in file:
            parts = line.split(":", 1)
            token, regex = parts

            token = token.strip()  

            #[A-z][A-z|0-9]*
            regex = regex.strip()
            regex_parts = regex.split("]", 1)

            if "[" in regex:
                regex_parts[0] = regex_parts[0]+"]"
                tokens[token] = regex_parts

                #Substituir a regex por uma regra
                for i in range(len(tokens[token])):  #['[A-z]', '[A-z|0-9]*'] || ['l','e','t']
                    tokens[token][i] = regex_to_rule(tokens[token][i]) # 
            else:
                tokens[token] = Rule(regex_to_rule(regex))
                
    return tokens
