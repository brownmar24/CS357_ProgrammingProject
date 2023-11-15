
#define operators
def is_star(char):
    return char == '*'

def is_plus(char):
    return char == '+'

def is_question(char):
    return char == '?'

def is_operator(char):
    return is_star(char) or is_plus(char) or is_question(char)


#define set notation
def is_open_set(char):
    return char == '['

def is_close_set(char):
    return char == ']'

def is_set(term):
    return is_open_set(term[0]) and is_close_set(term[-1])


def is_literal(char):
    return char.isalpha() or char.isdigit()


def is_unit(term):
    return is_literal(term[0]) or is_set(term)


def split_set(set_head):
    set_inside = set_head[1:-1]
    set_terms = list(set_inside)
    return set_terms


def split_expr(expr):
    head = None
    operator = None
    rest = None
    last_expr_pos = None

    if is_open_set(expr[0]):
        last_expr_pos = expr.find(']') + 1
        head = expr[0:last_expr_pos]
    elif is_literal(expr[0]):
        last_expr_pos = 1
        head = expr[0]

    if is_operator(expr[last_expr_pos]):
        operator = expr[last_expr_pos]
        last_expr_pos += 1

    rest = expr[last_expr_pos:] #+ 1:]
    return head, operator, rest

def does_unit_match(expr, string):
    head, operator, rest = split_expr(expr)

    if is_literal(head):
        return expr[0] == string[0]
    elif is_set(head):
        set_terms = split_set(head)
        return string[0] in set_terms

    return False


def match_expr(expr, string, match_length=0):
    if len(expr) == 0:
        return [True, match_length]
    
    head, operator, rest = split_expr(expr)
    
    if is_unit(head):
        if does_unit_match(expr, string):
            return match_expr(expr[1:], string[1:], match_length + 1)
    else:
        print('Unknown token in expr {expr}.')
    return [False, None]


def match(expr, string):
    match_pos = 0
    matched = False
    max_match_pos = len(string) - 1
    while not matched and match_pos < max_match_pos:
        [matched, match_length] = match_expr(expr, string[match_pos:])
        if matched:
            return [matched, match_pos, match_length]
        match_pos += 1
    return [False, None, None]


def main():
    expr = '[Hh][Ee]llo'
    string = 'HEllo'
    [matched, match_pos, match_length] = match(expr, string)
    if matched:
        print(f'match_expr({expr}, {string}) = {string[match_pos:match_pos + match_length]}')
    else:
        print(f'match_expr({expr}, {string}) = False')


if __name__ == '__main__':
    main()