from AST import(And,Or,Arrow,Not,Var,true,false, Pred, Forall, Exists)
from Exceptions import(LexException, ParseException)
from enum import Enum

def parse(text):
    return expr(lex(text))

####################################################################
# Lexer
# converts a string of characters into a list of tokens
# so "a && b -> T"
# becomes [Token(TVAR,0,"a"), Token(TAND,2), Token(TVAR,5,"b"),
#          Token(TARROW,7), Token(TTRUE,10)]
####################################################################


class TType(Enum):
    TTRUE   = "T"
    TFALSE  = "F"
    TNOT    = "~"
    TAND    = "&&"
    TOR     = "||"
    TARROW  = "->"
    TVAR    = "<var>"
    TLPAREN = "("
    TRPAREN = ")"
    TEOF    = "<EOF>"
    TEX     = "EX"
    TFA     = "FA"
    TDOT    = "."
    TCOMMA  = ","
    def __init__(self, n):
        self.n = n
    def __str__(self):
        return self.n

class Token():
    def __init__(self, ttype, pos, val):
        self.ttype = ttype
        self.pos = pos
        self.val = val
    def __str__(self):
        return str(self.ttype)

def alpha(c):
    return 'a' <= c <= 'z' or 'A' <= c <= 'Z'


def lex(text):
    i = 0
    tokens = []
    while i < len(text):
        c = text[i]
        if i+1 < len(text):
            n = text[i+1]
        else:
            n = ""

        if c in " \r\n\t": # skip whitespace
            pass
        elif c+n == "FA":
            tokens.append(Token(TType.TFA,i,"FA"))
            i += 1
        elif c+n == "EX":
            tokens.append(Token(TType.TEX,i,"EX"))
            i += 1
        elif c == 'T':
            tokens.append(Token(TType.TTRUE,i,"T"))
        elif c == 'F':
            tokens.append(Token(TType.TFALSE,i,"F"))
        elif c == '~':
            tokens.append(Token(TType.TNOT,i,"~"))
        elif c == '(':
            tokens.append(Token(TType.TLPAREN,i,"("))
        elif c == ')':
            tokens.append(Token(TType.TRPAREN,i,")"))
        elif c == '.':
            tokens.append(Token(TType.TDOT,i,"."))
        elif c == ',':
            tokens.append(Token(TType.TCOMMA,i,","))
        elif c+n == "||":
            tokens.append(Token(TType.TOR,i,"||"))
            i += 1
        elif c+n == "&&":
            tokens.append(Token(TType.TAND,i,"&&"))
            i += 1
        elif c+n == "->":
            tokens.append(Token(TType.TARROW,i,"->"))
            i += 1
        elif alpha(c):
            j = 0
            var = ""
            while i+j < len(text) and alpha(text[i+j]):
                var += text[i+j]
                j += 1
            tokens.append(Token(TType.TVAR,i,var))
            i += (j-1)

        else:
            raise LexException(i,c)

        i += 1
    tokens.append(Token(TType.TEOF,i,"<EOF>"))
    return tokens

# E => FA x . E | EX x . E | I
# I => O -> I
# O => A || O
# A => N && A
# N => !L
# L => var | T | F | (E)

def expr(tokens):
    follow = [TType.TEOF, TType.TRPAREN]
    e = None
    if tokens[0].ttype == TType.TFA:
        if tokens[1].ttype == TType.TVAR:
            if tokens[2].ttype == TType.TDOT:
                tokens.pop(0)
                v = tokens.pop(0).val
                tokens.pop(0)
                e = Forall(v,expr(tokens))
            else:
                raise ParseException(tokens[2].pos,[TType.TDOT],tokens[2].val)
        else:
            raise ParseException(tokens[1].pos,[TType.TVAR],tokens[1].val)
    elif tokens[0].ttype == TType.TEX:
        if tokens[1].ttype == TType.TVAR:
            if tokens[2].ttype == TType.TDOT:
                tokens.pop(0)
                v = tokens.pop(0).val
                tokens.pop(0)
                e = Exists(v,expr(tokens))
            else:
                raise ParseException(tokens[2].pos,[TType.TDOT],tokens[2].val)
        else:
            raise ParseException(tokens[1].pos,[TType.TVAR],tokens[1].val)
    else:
        e = arrow_expr(tokens)
    if tokens[0].ttype not in follow:
        raise ParseException(tokens[0].pos,follow,tokens[0].val)
    return e

def arrow_expr(tokens):
    follow = [TType.TEOF, TType.TRPAREN]
    lhs = or_expr(tokens)
    if tokens[0].ttype == TType.TARROW:
        tokens.pop(0)
        rhs = arrow_expr(tokens)
        lhs = Arrow(lhs, rhs)
    if tokens[0].ttype not in follow:
        raise ParseException(tokens[0].pos,follow,tokens[0].val)
    return lhs


def or_expr(tokens):
    follow = [TType.TEOF, TType.TRPAREN, TType.TARROW]
    lhs = and_expr(tokens)
    while tokens[0].ttype == TType.TOR:
        tokens.pop(0)
        rhs = and_expr(tokens)
        lhs = Or(lhs, rhs)
    if tokens[0].ttype not in follow:
        raise ParseException(tokens[0].pos,follow,tokens[0].val)
    return lhs

def and_expr(tokens):
    follow = [TType.TEOF, TType.TRPAREN, TType.TARROW, TType.TOR]
    lhs = not_expr(tokens)
    while tokens[0].ttype == TType.TAND:
        tokens.pop(0)
        rhs = not_expr(tokens)
        lhs = And(lhs, rhs)
    if tokens[0].ttype not in follow:
        raise ParseException(tokens[0].pos,follow,tokens[0].val)
    return lhs


def not_expr(tokens):
    follow = [TType.TEOF, TType.TRPAREN, TType.TARROW, TType.TOR, TType.TAND]
    e = None
    if tokens[0].ttype == TType.TNOT:
        tokens.pop(0)
        ne = not_expr(tokens)
        e = Not(ne)
    else:
        e = term(tokens)
    if tokens[0].ttype not in follow:
        raise ParseException(tokens[0].pos,follow,tokens[0].val)
    return e

def term(tokens):
    first = [TType.TTRUE, TType.TFALSE, TType.TVAR, TType.TLPAREN]
    follow = [TType.TEOF, TType.TRPAREN, TType.TARROW, TType.TOR, TType.TAND]

    e = None
    if tokens[0].ttype == TType.TVAR:
        e = pred(tokens)
    elif tokens[0].ttype == TType.TTRUE:
        e = true()
        tokens.pop(0)
    elif tokens[0].ttype == TType.TFALSE:
        e = false()
        tokens.pop(0)
    elif tokens[0].ttype == TType.TLPAREN:
        tokens.pop(0)
        e = expr(tokens)
        if tokens[0].ttype != TType.TRPAREN:
            raise ParseException(tokens[0].pos,[TType.TRPAREN],tokens[0].val)
        tokens.pop(0)
    elif tokens[0].ttype == TType.TFA or \
         tokens[0].ttype == TType.TEX:
         e = expr(tokens)
    else:
        raise ParseException(tokens[0].pos,first,tokens[0].val)

    if tokens[0].ttype not in follow:
        raise ParseException(tokens[0].pos,follow,tokens[0].val)
    return e

# ( v (, v)* )
def pred(tokens):
    follow = [TType.TEOF, TType.TRPAREN, TType.TARROW, TType.TOR, TType.TAND]
    e = None
    # initial name
    name = tokens.pop(0).val
    # P(v {, v} )
    if tokens[0].ttype == TType.TLPAREN:
        tokens.pop(0)
        vs = []
        if tokens[0].ttype == TType.TVAR:
            vs = [tokens.pop(0).val]
        # P()
        elif tokens[0].ttype == TType.TRPAREN:
            pass
        else:
            raise ParseException(tokens[0].pos, [TType.TVAR], tokens[0].val)

        # {, v}
        while tokens[0].ttype != TType.TRPAREN:
            if tokens[0].ttype == TType.TCOMMA and \
               tokens[1].ttype == TType.TVAR:
                tokens.pop(0)
                vs.append(tokens.pop(0).val)
            else:
                raise ParseException(tokens[0].pos, [TType.TCOMMA], tokens[0].val)
        tokens.pop(0)

        e = Pred(name, vs)
    # v
    else:
        e = Var(name)
    if tokens[0].ttype not in follow:
        raise ParseException(tokens[0].pos,follow,tokens[0].val)
    return e
