import lexer as L


class Term(object):
    pass


class Add(Term):
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2

    def __str__(self):
        return "(%s + %s)" % (self.t1, self.t2)


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


class Parser(object):
    def __init__(self, token):
        self.token = token

    def parse(self):
        try:
            term = self.term()
        except (ParseError, IndexError):
            raise ParseError

        if len(self.token) != 0:
            raise ParseError
        return term

    def try_parse(self, parsers):
        token = self.token
        try:
            return parsers[0]()
        except ParseError:
            self.token = token
            if len(parsers) != 0:
                return self.try_parse(parsers[1:])
            else:
                raise ParseError

    def consume(self, c):
        if len(self.token) == 0:
            raise ParseError
        elif self.token[0].__class__ == c:
            self.token = self.token[1:]
        else:
            raise ParseError

    def term(self):
        def add():
            t1 = self.form()
            self.consume(L.Plus)
            t2 = self.term()
            return Add(t1, t2)

        print(list(map(str, self.token)))
        return self.try_parse([add, self.form])

    def form(self):
        def num():
            head = self.token[0]
            self.consume(L.Num)
            return Num(head.value)

        def paren():
            self.consume(L.LParen)
            term = self.term()
            self.consume(L.RParen)
            return term

        return self.try_parse([paren, num])
