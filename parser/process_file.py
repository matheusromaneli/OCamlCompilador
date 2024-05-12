from scanner.automaton import Token

tokens = [Token(0,0,"<if-stmt>", "if", 2), Token(0,0,"<exp>","0", 0), Token(0,0,"if-stmt","if", 0), Token(0,0,"exp","1", 0), Token(0,0,"stmt","other", 0), Token(0,0,"else-stmt","else", 0), Token(0,0,"stmt","other", 0)]

rules = {
    1: ("<stmt>", "<if-stmt>"),
    2:("<stmt>","other"),
    3:("<if-stmt>","if (<exp>) <stmt> <else-stmt>"),
    4:("<else-stmt>","else <stmt>"),
    5:("<else-stmt>",""),
    6:("<exp>","0"),
    7:("<exp>","1"),
}

look_ahead = {
    "<stmt>": {
        "if": 1,
        "other": 2,
    },
    "<if-stmt>":{
        "if": 3,
    },
    "<else-stmt>":{
        "else":4,
        "": 5,
    },
    "<exp>":{
        "0": 6,
        "1": 7,
    }
}

def parser(tokens: list["Token"], look_ahead):
    pile =  look_ahead[("expr",tokens[0].ttype)]
    tokens.pop(0)
    curr_type = "expr"
    print(tokens)
    print(pile)
    # for token in tokens:
    #     current_rule = look_ahead[][token.ttype]
    #     pile = current_rule + pile
                
