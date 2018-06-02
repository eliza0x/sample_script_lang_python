import parser as P


def eval_term(term):
    if term.__class__ == P.Add:
        return eval_term(term.t1) + eval_term(term.t2)
    elif term.__class__ == P.Num:
        return term.value
    else:
        pass
