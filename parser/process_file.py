from scanner.automaton import Token    


def parser(tokens: list["Token"], pile: list, look_ahead, depth):
    space = "\t" * depth
    print(space,"TOKENS:", tokens)
    print(space, "PILE:",pile)
    curr_token = tokens[0]
    if curr_token.ttype == "EOF" or curr_token.ttype == "EOL" or pile == [] or pile[0] == 'epsilon':
        return True, 1
    curr_expr = pile[0]
    curr_rule = look_ahead[curr_expr]
    if not curr_rule:
        if(curr_token.ttype == curr_expr or curr_token.tvalue == curr_expr) : # terminal
            print(space, "Token readed:", curr_token.tvalue)
            return parser(tokens[1:], pile[1:], look_ahead, depth+1) # token readed
        if(curr_expr.startswith("[")): #optional
            # print("Skipping... ", curr_expr)
            return parser(tokens, pile[1:], look_ahead, depth+1) # token skipped

    result = 0
    # for option in curr_rule.keys():
    #   if option == curr_token.tvalue or option == curr_token.ttype: # non-terminal     
    print(space,"Possible rules: ", curr_rule[curr_token.ttype])    
    for next_rule in curr_rule[curr_token.ttype]:
        success = False
        for rule_index in range(len(next_rule)):
            rule = next_rule[rule_index]
            success, tokens_accepted = parser(tokens[result:], [rule], look_ahead, depth+1)
            if not success:
                break
            result += tokens_accepted
            print(space, "result(",rule,"):", result)
        if success:
            return True, result
    
    print(space, "Unexpected", curr_token.tvalue, "at position:", curr_token.start)
    return 0, 0