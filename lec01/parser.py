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


'''
T  ::= V '+' F | F | empty

F  ::= (T) | number
'''


def parse(token):
    next_token, term = term_parser(token)
    if len(next_token) != 0:
        raise ParseError
    return term


def try_parse(token, parsers):
    try:
        return parsers[0](token)
    except ParseError:
        if len(parsers) != 0:
            return try_parse(token, parsers[1:])
        else:
            raise ParseError


def consume(token, c):
    if len(token) == 0:
        raise ParseError
    elif token[0].__class__ == c:
        return token[1:]
    else:
        raise ParseError


def term_parser(token):
    def add_parser(token):
        next_token, t1 = form_parser(token)
        next_token = consume(next_token, L.Plus)
        next_token, t2 = term_parser(next_token)
        return next_token, Add(t1, t2)

    print(list(map(str, token)))
    return try_parse(token, [add_parser, form_parser])


def form_parser(token):
    def num_parser(token):
        next_token = consume(token, L.Num)
        return next_token, Num(token[0].form)

    def paren_parser(token):
        next_token = consume(token, L.LParen)
        next_token, term = term_parser(next_token)
        next_token = consume(next_token, L.RParen)
        return next_token, term

    return try_parse(token, [paren_parser, num_parser])
