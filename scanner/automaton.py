from read_regex import Rule


class State:

    def __init__(self) -> None:
        self.transitions = []

    def add_transition(self, new_transition: "Transition"):
        self.transitions.append(new_transition)

    def has_transition_for(self, char: str):
        for transition in self.transitions:
            if transition.rule == char:
                return transition
        return None

class Transition:
    def __init__(self, state: "State", rule: "Rule"):
        self.state = state
        self.rule = rule

 

class Automaton:
    def __init__(self, rules: list["Rule"], name: str="default"):
        self.states = [State()]
        curr_state=0
        for rule in rules:

            if rule.repeatable:
                next_state = curr_state
            else:
                self.states.append(State())
                next_state = curr_state + 1

            new_transition = Transition(self.state[next_state], rule)
            self.states[curr_state].add_transition(new_transition)
            
            curr_state += 1

    def match(self, word: str):
        curr_state = self.states[0]
        length_matched = 0
        for letter in word:
            transition = curr_state.has_transition_for(letter)
            if transition is None:
                return length_matched
            curr_state = transition.state
            length_matched += 1
        return length_matched
    
def read_tokens(tokens: dict[str, list["Rule"]]):
    automatons = []
    for name,rules in tokens.items():
        new_auto = Automaton(rules, name)
        automatons.append(new_auto)
    return automatons
