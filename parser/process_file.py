from scanner.automaton import Token    


# def parser(tokens: list["Token"], pile: list, look_ahead):
#     print("Current pile:", pile)
#     curr_token = tokens[0]
#     if curr_token.ttype == "EOF":
#         return True
#     curr_expr = pile[0]
#     curr_rule = look_ahead[curr_expr]
#     print("Currents:")
#     print("\ttoken: ", curr_token)
#     print("\texpr: ", curr_expr)
#     print("\trules: ", curr_rule)
#     print()
#     if not curr_rule:
#         if(curr_token.ttype == curr_expr or curr_token.tvalue == curr_expr): # terminal
#             print("Token readed:", curr_token.tvalue)
#             return parser(tokens[1:], pile[1:], look_ahead) # token readed
#         if(curr_expr.startswith("[")): #optional
#             print("Skipping... ", curr_expr)
#             return parser(tokens, pile[1:], look_ahead) # token skipped

#     result = False
#     for option in curr_rule.keys():
#         if option == curr_token.tvalue or option == curr_token.ttype: # non-terminal            
#             next_rule = curr_rule[option]
#             print("read exp:", curr_expr, "with token:", curr_token.tvalue)
#             result = parser(tokens, next_rule + pile[1:], look_ahead) # branch rule
    
#         if result is True:
#             return True
    
#     print("Unexpected", curr_token.tvalue, "at position:", curr_token.start)
#     return False
def parser(tokens, lookahead_table):
    stack = ["let-definition"]
    index = 0
    while stack:
        top = stack[-1]  # Olha o último item da pilha sem remover
        if index < len(tokens):
            token = tokens[index]
        else:
            break

        if top == token:
            stack.pop()  # Remove da pilha se o token corresponde ao topo da pilha
            index += 1
        elif top in lookahead_table and token in lookahead_table[top]:
            stack.pop()  # Remove o topo da pilha
            # Adiciona os itens da produção na pilha em ordem reversa
            stack.extend(reversed(lookahead_table[top][token]))
        else:
            return False, f"Unexpected token {token} at position: {index}"

    # Verifica se todos os tokens foram consumidos e a pilha está vazia
    if index == len(tokens) and not stack:
        return True, "Parsing successful"
    else:
        return False, "Parsing failed, stack or tokens left"

# Vamos executar novamente o parser ajustado
# parser(test_tokens, lookahead.table)
