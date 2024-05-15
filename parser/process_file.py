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

def parser(tokens: list["Token"], look_ahead, curr_token: str, pile: list):
    print(curr_token, tokens[0].tvalue,"\t\t", pile)
    if tokens[0].ttype == "EOF": return True
    if curr_token[0].isalpha():
        options = look_ahead[curr_token].keys()
        result = False
        for option in options:
            curr_rule = look_ahead[curr_token][option]
            print("Current rule:", curr_rule)
            print("Current option:", option)
            if tokens[0].tvalue == option or tokens[0].ttype == option: # aplica regra do token
                print("Accepted token:", tokens[0].tvalue)
                result = parser(tokens[1:], look_ahead, option, curr_rule[1:]+pile[1:])
            if result is False: # entra na regra até o terminal
                result = parser(tokens, look_ahead, option, curr_rule+pile[1:])

            if result == True:
                return True
        return False   
    elif len(pile)>0 and pile[0].startswith("[") and pile[0].endswith("]"):
        print("Optional parameter:", pile[0])
        if tokens[0].tvalue == pile[0]:
            print("Accepted token:", tokens[0].tvalue)
            result = parser(tokens[1:], look_ahead, pile[1], pile[1:])
        else:
            result = parser(tokens, look_ahead, pile[1], pile[1:])
    