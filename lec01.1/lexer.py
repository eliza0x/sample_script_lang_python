class Token(object):
    pass


class Plus(Token):
    def __str__(self):
        return "Plus"


class RParen(Token):
    def __str__(self):
        return ")"


class LParen(Token):
    def __str__(self):
        return "("


class Num(Token):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Num(%s)" % self.value


'''
プログラムに現れる記号列を分解
'1 + ( 2 + 3 )'
↓
[N(1), Add, '(', '2', '+', '3', ')']
'''


def lex(source):
    def spanDigits(source):
        digits, i = [(source[:i], i)
                     for i in range(1, 1+len(source))
                     if source[:i].isdigit()][-1]
        return digits, source[i:]

    if len(source) == 0:
        return []

    elif source[0].isdigit():
        digits, nextSource = spanDigits(source)
        return [Num(int(digits))] + lex(nextSource)

    elif source[0] == '(':
        return [LParen()] + lex(source[1:])

    elif source[0] == ')':
        return [RParen()] + lex(source[1:])

    elif source[0] == '+':
        return [Plus()] + lex(source[1:])

    elif source[0] == ' ':
        return lex(source[1:])

    else:
        pass
