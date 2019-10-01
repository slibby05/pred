from sys import argv
from AST import (Pred, Forall, Exists, Var, true, false, And, Or, Not, Arrow)
from Parser import parse
from Exceptions import (ProofException, SubException, ParseException, LexException)
from Proof import (clear, step, premise, andI, andEL, andER, \
                   orIL, orIR, orE, assume, assumed, arrowI, arrowE, \
                   notI, notE, TI, FE, LEM, \
                   forallI, forallE, existsI, existsE)

def main():
    try:
        expr = parse(argv[1])
        print(str(expr))
        example().print_proof()
    except (SubException, ParseException, LexException) as e:
        print(str(e))
    except (ProofException) as e:
        e.print()


##################################################################
# Example of a proof of the commutativity of ∀ 
# ∃ x . ∀ y . P(x,y) |- ∀ y . ∃ x . P(x,y) 
# 
#                                          [∀ y. P(u,y)]
#                                          ------------- ∀ E
#                                             P(u,v) 
#                                          ------------- ∃ I
#                                     [v]   ∃ x. P(x,v) 
#                                     ------------------ ∀ I
#                    [∀ y. P(u,y)]     ∀ y. ∃ x. P(x,y) 
#                    ----------------------------------- → I
# ∃ x. ∀ y. P(x,y)   (∀ y. P(u,y)) → (∀ y. ∃ x. P(x,y))
# ------------------------------------------------------ ∃ E
#                   ∀ y. ∃ x. P(x,y)
#
# Note: we need to stare every proof with clear()
# This is a hack to get things to work out right.
##################################################################
def example():
    clear()
    p1 = premise(parse("EX x. FA y. P(x,y)"))
    a1 = assume(parse("FA y. P(u,y)"))

    a2 = assume(Var("v"))
    l1 = assumed(parse("FA y. P(u,y)"))
    l2 = forallE(l1, "v", parse("P(u,v)"))
    l3 = existsI(l2, "u", parse("EX x. P(x,v)"))
    l4 = forallI(a2, l3, parse("FA y. EX x. P(x,y)"))

    l5 = arrowI(a1, l4, parse("(FA y. P(u,y)) -> (FA y. EX x. P(x,y))"))
    l6 = existsE(p1, "u", l5, parse("FA y. EX x. P(x,y)"))
    return l6

if __name__ == "__main__":
    main()
