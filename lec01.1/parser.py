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
T  ::= F '+' T | F | empty

F  ::= (T) | number
'''


class Parser(object):
    def __init__(self, token):
        self.token = token

    def parse(self):
        try:
            term = self.term()
        except (ParseError):
            raise ParseError

        if not(self.is_token_empty()):
            raise ParseError
        return term

    def next_token(self):
        return self.token[0]

    def is_token_empty(self):
        return len(self.token) == 0

    def try_parse(self, parsers):
        token = self.token
        if self.is_token_empty:
            try:
                return parsers[0]()
            except ParseError:
                self.token = token
                return self.try_parse(parsers[1:])
        else:
            raise ParseError

    def match(self, c):
        def consume_token():
            self.token = self.token[1:]

        if self.is_token_empty():
            raise ParseError
        elif self.next_token().__class__ == c:
            consume_token()
        else:
            raise ParseError

    def term(self):
        def add():
            t1 = self.form()
            self.match(L.Plus)
            t2 = self.term()
            return Add(t1, t2)

        print(list(map(str, self.token)))
        return self.try_parse([add, self.form])

    def form(self):
        def num():
            head = self.next_token()
            self.match(L.Num)
            return Num(head.value)

        def paren():
            self.match(L.LParen)
            term = self.term()
            self.match(L.RParen)
            return term

        return self.try_parse([paren, num])
