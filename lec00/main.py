from lexer import lex
from parser import parse
from eval import eval_term


def main():
    source = input()
    token = lex(source)
    print(list(map(str, token)))
    term = parse(token)
    print(term)
    ans = eval_term(term)
    print('ans: '+str(ans))


if __name__ == '__main__':
    main()
