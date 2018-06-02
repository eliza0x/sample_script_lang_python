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




# 与えられたクラスとトークンが一致することを確認、一致していれば消費、一致しなければ例外を投げる
def consume(token, c):
    if len(token) == 0:
        raise ParseError
    elif token[0].__class__ == c:
        return token[1:]
    else:
        raise ParseError


def parse(token):
    next_token, term = term_parser(token)
    # パースが終了した状態でトークン列を消費しきれていない場合エラー状態
    if len(next_token) != 0:
        raise ParseError
    return term


'''
BNFでググると良い

T ::= number '+' T
    | number
'''


# 式
def term_parser(token):
    print(list(map(str, token)))
    # 初めに和の式だとしてパース
    try:
        return plus_parser(token)
    except ParseError:
        # 失敗すれば数値だとして処理
        try:
            return num_parser(token)
        except ParseError:
            # それでも失敗するならパース失敗
            raise ParseError


# 和
def plus_parser(token):
    # 初めに数値
    next_token, t1 = num_parser(token)
    # 次に'+'
    next_token = consume(token, L.Plus)
    # 次に式
    next_token, t2 = term_parser(next_token)
    return next_token, Add(t1, t2)

# 数値
def num_parser(token):
    next_token = consume(token, L.Num)
    return next_token, Num(token[0].value)
