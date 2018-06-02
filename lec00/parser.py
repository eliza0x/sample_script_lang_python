import lexer as L


class Term(object):
    pass


class Add(Term):
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2

    def __str__(self):
        return "(%s) + (%s)" % (self.t1, self.t2)


class Num(Term):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "%s" % self.value


class ParseError(Exception):
    pass


def consume(token, c):
    if len(token) == 0:
        raise ParseError
    elif token[0].__class__ == c:
        return token[1:]
    else:
        raise ParseError


def parse(token):
    next_token, term = term_parser(token)
    if len(next_token) != 0:
        raise ParseError
    return term


'''
T ::= number '+' T
    | number
'''


def term_parser(token):
    print(list(map(str, token)))
    try:
        return plus_parser(token)
    except ParseError:
        try:
            return num_parser(token)
        except ParseError:
            raise ParseError


def plus_parser(token):
    next_token, t1 = num_parser(token)
    next_token = consume(token, L.Plus)
    next_token, t2 = term_parser(next_token)
    return next_token, Add(t1, t2)


def num_parser(token):
    next_token = consume(token, L.Num)
    return next_token, Num(token[0].value)
