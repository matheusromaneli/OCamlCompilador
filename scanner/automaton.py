from io import BufferedReader
from .read_regex import Rule


class State:

    def __init__(self, name: str="default") -> None:
        self.transitions = []
        self.name = name

    def add_transition(self, new_transition: "Transition"):
        self.transitions.append(new_transition)

    def has_transition_for(self, char: str):
        for transition in self.transitions:
            if transition.rule == char:
                return transition.state
        return None
    
    def __str__(self):
        return f"""
        \t\t{self.name}:
        \t\t\t{self.transitions}
        """

    def __repr__(self):
        return self.__str__()

class Transition:
    def __init__(self, state: "State", rule: "Rule"):
        self.state = state
        self.rule = rule

    def __str__(self) -> str:
        return f"'{self.rule}' -> {self.state.name}"
    
    def __repr__(self) -> str:
        return self.__str__()
 
class Token:
    def __init__(self, start, end, token_type, token_value, size) -> None:
        self.start = start
        self.end = end
        self.ttype = token_type
        self.tvalue = str(token_value)
        self.size = size 

    def __repr__(self) -> str:
        return f"<{self.ttype}>, ({self.tvalue})"

class Automaton:
    def __init__(self, exp_rules: list[list["Rule"]], name: str="default"):
        self.states = [State("0")]
        self.name = name
        state_size = 0
        for rules in exp_rules:
            curr_state = 0
            for rule in rules:
                if rule.repeatable:
                    next_state = curr_state
                else:
                    next_state = state_size + 1
                    self.states.append(State(f"{next_state}"))
                    state_size += 1
                new_transition = Transition(self.states[state_size], rule)
                self.states[curr_state].add_transition(new_transition)
                curr_state = next_state

    def match(self, file: BufferedReader) -> Token:
        token_value = ""
        start = file.tell()

        curr_state = self.states[0]
        _input = file.read(1).decode()
        curr_state = curr_state.has_transition_for(_input)
        token_value += _input

        while curr_state is not None:
            _input = file.read(1).decode()
            curr_state = curr_state.has_transition_for(_input)
            token_value += _input

        end = file.tell()

        if _input == '':
            end += 1
        else:
            end -= 1
            token_value = token_value[:-1]

        size = end - start
        return Token(start, end, self.name, token_value[:], size)
    
    def __str__(self):
        return f"""
        {self.name}:
        \tstates:
        \t{self.states}
        """
    
    def __repr__(self) -> str:
        return self.__str__()

def create_automatons(tokens: dict[str, list[list["Rule"]]]):
    automatons = []
    for name,rules in tokens.items():
        new_auto = Automaton(rules, name)
        automatons.append(new_auto)
    return automatons
