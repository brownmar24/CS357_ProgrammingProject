#Shows character to start with. ^ must occur before character (Ex: ^a)
def start(char):
    return char == '^'

#Ends with specific character. $ must come after character (EX: a$) 
def end(char):
    return char == '$'

#Zero or more occurences of character. Comes after character (EX: a*)
def is_star(char):
    return char == '*'

#One or more instances
def plus(char):
    return char == '+'

#Zero or one occurences
def question(char):
    return char == '?'

def is_op(char):
    return is_star(char) or plus(char) or question(char)

#Matches with any character
def dot(char):
    return char == '.'

#Open and close of a regex. Helps with priority and groupings
def open_paren(char):
    return char == '('
def close_paren(char):
    return char == ')'

#Open and close for sets. Set notation
def open_set(char):
    return char == '['
def close_set(char):
    return char == ']'

def is_literal(char):
    return char.isalpha() or char.isdigit() or char in ' :/'

def is_alternate(term):
    return open_paren(term[0]) and close_paren(term[-1])

def is_set(term):
    return open_set(term[0]) and close_set(term[-1])

def is_unit(term):
    return is_literal(term[0]) or dot(term[0]) or is_set(term)

def split_alternate(alternate):
    return alternate[1:-1].split('|')

def split_set(set_head):
    set_inside = set_head[1:-1]
    set_terms = list(set_inside)
    return set_terms

def split_regex(regex):
    head = None
    operator = None
    rest = None
    last_regex_pos = 0

    if open_set(regex[0]):
        last_regex_pos = regex.find(']') + 1
        head = regex[:last_regex_pos]
    elif open_paren(regex[0]):
        last_regex_pos = regex.find(')') + 1
        head = regex[:last_regex_pos]
    #    head = regex[:2]
    else:
        last_regex_pos = 1
        head = regex[0]

    if last_regex_pos < len(regex) and is_op(regex[last_regex_pos]):
        operator = regex[last_regex_pos]
        last_regex_pos += 1

    rest = regex[last_regex_pos:]

    return head, operator, rest


def does_unit_match(regex, string):
    head, operator, rest = split_regex(regex)

    if len(string) == 0:
        return False
    if is_literal(head):
        return regex[0] == string[0]
    elif dot(head):
        return True
    elif is_set(head):
        set_terms = split_set(head)
        return string[0] in set_terms

    return False


def match_multiple(regex, string, match_length, min_match_length=None, max_match_length=None):
    head, operator, rest = split_regex(regex)

    if not min_match_length:
        min_match_length = 0

    submatch_length = -1

    while not max_match_length or (submatch_length < max_match_length):
        [subregex_matched, subregex_length] = match_regex(
            (head * (submatch_length + 1)), string, match_length
        )
        if subregex_matched:
            submatch_length += 1
        else:
            break

    while submatch_length >= min_match_length:
        [matched, new_match_length] = match_regex(
            (head * submatch_length) + rest, string, match_length
        )
        if matched:
            return [matched, new_match_length]
        submatch_length -= 1

    return [False, None]


def match_star(regex, string, match_length):
    return match_multiple(regex, string, match_length, None, None)


def match_plus(regex, string, match_length):
    return match_multiple(regex, string, match_length, 1, None)


def match_question(regex, string, match_length):
    return match_multiple(regex, string, match_length, 0, 1)


def match_alternate(regex, string, match_length):
    head, operator, rest = split_regex(regex)
    options = split_alternate(head)

    for option in options:
        [matched, new_match_length] = match_regex(
            option + rest, string, match_length
        )
        if matched:
            return [matched, new_match_length]

    return [False, None]


def match_regex(regex, string, match_length=0):
    if len(regex) == 0:
        return [True, match_length]
    elif end(regex[0]):
        if len(string) == 0:
            return [True, match_length]
        else:
            return [False, None]

    head, operator, rest = split_regex(regex)

    if is_star(operator):
        return match_star(regex, string, match_length)
    elif plus(operator):
        return match_plus(regex, string, match_length)
    elif question(operator):
        return match_question(regex, string, match_length)
    elif is_alternate(head):
        return match_alternate(regex, string, match_length)
    elif is_unit(head):
        if does_unit_match(regex, string):
            return match_regex(rest, string[1:], match_length + 1)
    else:
        print(f'Invalid regexession! Please reference the Infographic {regex}.')

    return [False, None]


def match(regex, string):
    match_pos = 0
    matched = False
    if start(regex[0]):
        max_match_pos = 0
        regex = regex[1:]
    else:
        max_match_pos = len(string) - 1
    while not matched and match_pos <= max_match_pos:
        [matched, match_length] = match_regex(regex, string[match_pos:])
        if matched:
            return [matched, match_pos, match_length]
        match_pos += 1
    return [False, None, None]      

def main():
    regex = '^[ABC][abc]+[012][012][012][012]$'
    string = 'Ab1201'
    [matched, match_pos, match_length] = match(regex, string)
    if matched:
        #print(f'match_regex({regex}, {string}) = {string[match_pos:match_pos + match_length]}')
        print(f'match regex: {regex}, string: {string} This test string CAN be generated by the given regex.')
    else:
        #print(f'match_regex({regex}, {string}) = False')
        print(f'match regex: {regex}, string: {string} This test string CANNOT be generated by the given regex.')

#A-Z All capital alphabet: ABCDEFGHIJKLMNOPQRSTUVWXYZ
#a-z All lowercase alphabet: abcdefghijklmnopqrstuvwxyz
#0-9 Digits: 0123456789
if __name__ == '__main__':
    main()