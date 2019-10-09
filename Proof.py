from AST import(Node,And,Or,Arrow,Not,Var,true,false, Forall, Exists, Pred)
from Exceptions import ProofException

####################################################################################
# This is a very small, and probably bad, proof checker for propositional logic
# The proof rules are the same ones we have in class.
#
#  A  B      A ∧ B      A ∧ B 
# ------∧ I ------∧ EL ------∧ ER
# A ∧ B        A          B
#
#    A         B         A ∨ B A →  C B →  C
# ------∨ IL ------∨ IR --------------------∨ E
# A ∨ B      A ∨ B               C
# 
# [A] B        A  A →  B
# ------ → I  ----------- → E
# A →  B           B
# 
# A →  F      A  ¬A
# ------ ¬I  ------- ¬E
#   ¬A          F
# 
#               F
# ----- TI   ------ FE  --------- LEM
#   T           A        A ∨ ¬A
#
# [c] P        Ax.P
# ------ AI  --------- AE
#  Ax.P        P[x→ c]
#
#    A     Ex.A[x]  A[c]→ B
# ------EI -----------------EE
#  Ex.A           B

# Each of the proof rules have a corresponding function
# so AndI() is the function for ∧ I rule
####################################################################################

##########################################
# 
# ------- Premise
#    A
#
# input e: any expression
# ouput: a proof of e
# careful, this will be added to the premises list
# so really you're proving e |- e
##########################################
def premise(e):
    global premises
    s = step(e,"Premise", [])
    premises.append(s)
    return s

##########################################
#  A  B     
# ------∧ I
# A ∧ B
#
# input a: a proof for A
# input b: a proof for B
# input ab: the expression And(A,B)
# output: a proof for And(a,b)
#
##########################################
def andI(a, b, ab):
    ret = step(ab, "∧ I", [a,b])
    if ab.type() != Node.AND:
        raise ProofException("∧ I", ab, "conclusion is not in the form A ∧ B", ret)
    if ab.lhs != a.expr:
        raise ProofException("∧ I", a.expr, "left hand side doesn't match conclusion", ret)
    if ab.rhs != b.expr:
        raise ProofException("∧ I", a.expr, "right hand side doesn't match conclusion", ret)
    return ret

##########################################
# A ∧ B     
# ------ ∧ EL
#    A       
#
# input ab: a proof for And(A,B)
# input a: the expression A
# output: a proof for A
#
##########################################
def andEL(ab, a):
    ret = step(a,"∧ EL", [ab])
    if ab.expr.type() != Node.AND:
        raise ProofException("∧ EL", ab.expr, "premise is not in the form A ∧ B", ret)
    if ab.expr.lhs != a:
        raise ProofException("∧ EL", a, "conslusion doesn't match left hand side of premise", ret)
    return ret

##########################################
# A ∧ B     
# ------ ∧ ER
#    B       
#
# input ab: a proof for And(A,B)
# input b: the expression B
# output: a proof for B
#
##########################################
def andER(ab, b):
    ret = step(b,"∧ ER", [ab])
    if ab.expr.type() != Node.AND:
        raise ProofException("∧ ER", ab.expr, "premise is not in the form A ∧ B", ret)
    if ab.expr.rhs != b:
        raise ProofException("∧ ER", b, "conslusion doesn't match right hand side of premise", ret)
    return ret

##########################################
#    A      
# ------∨ IL
# A ∨ B    
#
# input a: a proof for A
# input ab: the expression Or(A,B)
# output: a proof for Or(A,B)
#
##########################################
def orIL(a, ab):
    ret = step(ab,"∨ IL", [a])
    if ab.type() != Node.OR:
        raise ProofException("∨ IL", ab, "conclusion is not in the form A ∧ B", ret)
    if ab.lhs != a.expr:
        raise ProofException("∨ IL", a.expr, "left hand side of conclusion doesn't match premise", ret)
    return ret

##########################################
#    B      
# ------∨ IR
# A ∨ B    
#
# input a: a proof for B
# input ab: the expression Or(A,B)
# output: a proof for Or(A,B)
#
##########################################
def orIR(b, ab):
    ret = step(ab,"∨ IL", [b])
    if ab.type() != Node.OR:
        raise ProofException("∨ IR", ab, "conclusion is not in the form A ∧ B", ret)
    if ab.rhs != b.expr:
        raise ProofException("∨ IR", b.expr, "right hand side of conclusion doesn't match premise", ret)
    return ret

##########################################
# A∨ B A→ C B→ C
# ---------------∨ E
#       C              
#
# input ab: a proof for Or(A,B)
# input ac: a proof for Arrow(A,C)
# input bc: a proof for Arrow(B,C)
# input c: the expression C
# output: a proof for C
#
##########################################
def orE(ab, ac, bc, c):
    ret = step(c, "∨ E", [ab, ac, bc])
    if ab.expr.type() != Node.OR:
        raise ProofException("∨ E", ab.expr, "premise doesn't match A ∨ B", ret)
    if ac.expr.type() != Node.ARROW:
        raise ProofException("∨ E", ac.expr, "premise doesn't match A → C", ret)
    if bc.expr.type() != Node.ARROW:
        raise ProofException("∨ E", bc.expr, "premise doesn't match B → C", ret)
    if ab.expr.lhs != ac.expr.lhs:
        raise ProofException("∨ E", ab.expr, "A doesn't match: %s != %s" % (str(ab.expr.lhs), str(ac.expr.lhs)), ret)
    if ab.expr.rhs != bc.expr.lhs:
        raise ProofException("∨ E", ab.expr, "B doesn't match: %s != %s" % (str(ab.expr.rhs), str(bc.expr.lhs)), ret)
    if ac.expr.rhs != bc.expr.rhs:
        raise ProofException("∨ E", ac.expr, "C doesn't match: %s != %s" % (str(ac.expr.rhs), str(bc.expr.rhs)), ret)
    if ac.expr.rhs != c:
        raise ProofException("∨ E", c, "C doesn't match conclusion", ret)
    return ret

##########################################
# used in → I rule
# 
# -----Assume
#   a        
#
# input a: an expression A
# output: a proof that we assumed A
#
##########################################
def assume(a):
    assumptions.append(a)
    return step(a, "assume", [])

##########################################
# 
# -----Assumed
#   a        
#
# input a: an expression A
# output: a proof that we have already assumed A
# Note: this will fail we we haven't already assumed A in the proof
#
##########################################
def assumed(a):
    ret = step(a, "assumed", [])
    if a not in assumptions:
        raise ProofException("assumption", a, "conclusion has not yet been assumed", ret)
    return ret

##########################################
# [A] B     
# ------ → I
# A →  B    
#
# input a: a proof that we've assumed a
# input b: a proof of B that can use the assumption A
# input ab: a an expression A →  B
# output: a proof of A →  B
# Note: the removes A from the possible assumtions
#
##########################################
def arrowI(a, b, ab):
    ret = step(ab, "→ I", [a,b])
    if ab.type() != Node.ARROW:
        raise ProofException("→ I", ab, "conclusion doesn't match A → B", ret)
    if ab.lhs != a.expr:
        raise ProofException("→ I", a.expr, "left hand side doens't match conclusion", ret)
    if ab.rhs != b.expr:
        raise ProofException("→ I", b.expr, "right hand side doens't match conclusion", ret)
    if assumptions.pop() != a.expr:
        raise ProofException("→ I", a.expr, "A was not the last assumption made", ret)
    return ret

##########################################
#  A  A→ B     
# --------- → E
#    B
#
# input a: a proof a A
# input ab: a proof of A →  B
# input b: an expression B
# output: a proof of B
#
##########################################
def arrowE(a, ab, b):
    ret = step(b, "→ E", [a,ab])
    if ab.expr.type() != Node.ARROW:
        raise ProofException("→ E", ab.expr, "premise doesn't match A → B", ret)
    if ab.expr.lhs != a.expr:
        raise ProofException("→ E", a.expr, "left hand side doens't match", ret)
    if ab.expr.rhs != b:
        raise ProofException("→ E", b.expr, "conclusion doens't match right hand side", ret)
    return ret

##########################################
# A → F   
# ------ ¬I
#   ¬A     
#
# input af: a proof of A → F
# input na: a expression ¬A
# output: a proof of ¬A
#
##########################################
def notI(af, na):
    ret = step(na, "¬I", [af])
    if af.expr.type() != Node.ARROW or af.expr.rhs != false():
        raise ProofException("¬I", af.expr, "premise doesn't match A → F", ret)
    if Not(af.expr.lhs) != na:
        raise ProofException("¬I", na, "conclusion doesn't match premise", ret)
    return ret
        
##########################################
#  A  ¬A    
# ------- ¬E
#    F      
#
# input a: a proof of A
# input na: a proof of ¬A
# input f: a expression F
# output: a proof F
#
##########################################
def notE(a, na, f):
    ret = step(f, "¬E", [a,na])
    if na.expr.type() != Node.NOT:
        raise ProofException("¬E", na.expr, "premise doesn't match ¬A", ret)
    if na.expr.lhs != a.expr:
        raise ProofException("¬E", a.expr, "premises don't match", ret)
    if f != false():
        raise ProofException("¬E", f, "conclusion must be false", ret)
    return ret

##########################################
#           
# ------- TI
#    T      
#
# input t: the expression T
# output: a proof of T
#
##########################################
def TI(t):
    ret = step(t,"TI",[])
    if t != true():
        raise ProofException("TI", t, "conclusion must be true", ret)
    return ret

##########################################
#    F
# ------ FE
#    A     
#
# input f: a proof of F
# input a: an expression A
# output: a proof of A
#
##########################################
def FE(f, a):
    ret = step(a,"⊥ E",[f])
    if f.expr != false():
        raise ProofException("⊥ E", f.expr, "premise must be flase", ret)
    return ret

##########################################
# 
# --------- LEM
#  A ∨ ¬A
#
# input a: a expression (A ∨ ¬A)
# output: a proof of (A ∨ ¬A)
#
##########################################
def LEM(a):
    ret = step(a,"LEM",[])
    if a.type() != Node.OR or \
       a.rhs.type() != Node.NOT or \
       a.lhs != a.rhs.lhs:
        raise ProofException("LEM", a, "conclusion doens't match A ∨ ¬A", ret)
    return ret


##########################################
# [c]  A(c)
# ---------- ∀ I 
#  ∀ x.A(x)
#
#
# input c: an assumed variable
# input ac: a proof of A(c)
# input fax: the expression ∀ x. A(x)
# output: a proof for ∀ x. A(x)
#
##########################################
def forallI(c, ac, fax):
    ret = step(fax, "∀ I", [c,ac])
    if fax.type() != Node.FORALL:
        raise ProofException("∀ I", fax, "conclusion is not in the form ∀  x. A", ret)
    if c.expr.type() != Node.VAR:
        raise ProofException("∀ I", c.expr, "assumption must be a variable", ret)
    if fax.expr.sub(fax.var, c.expr.name) != ac.expr:
        raise ProofException("∀ I", fax.expr, "premise doesn't match conclusion", ret)
    if assumptions.pop() != c.expr:
        raise ProofException("∀ I", c.expr, "ins't the most recent assumption", ret)
    return ret

##########################################
#
#  ∀ x.A(x)
# --------- ∀ E
#    A(c)
#
# input fax: a proof of ∀ x. A(x)
# input c: a string with the replacement for x
# input ac: the expression A(c)
# output: a proof for A(c)
#
##########################################
def forallE(fax, c, ac):
    ret = step(ac, "∀ E", [fax])
    if fax.expr.type() != Node.FORALL:
        raise ProofException("∀ E", fax.expr, "premise is not in the form ∀  x. A", ret)
    if fax.expr.expr.sub(fax.expr.var, c) != ac:
        raise ProofException("∀ E", ac, "premise doesn't match conclusion", ret)
    return ret

##########################################
#
#    A(c)
# ---------∃ I
#  ∃ x.A(x)
#
# input ac: a proof of A(c)
# input c: a string with the c to replace
# input eax: the expression ∃ x. A(x)
# output: a proof for ∃ x. A(x)
#
##########################################
def existsI(ac, c, eax):
    ret = step(eax, "∃ I", [ac])
    if eax.type() != Node.EXISTS:
        raise ProofException("∃ I", eax, "premise is not in the form ∃  x. A", ret)
    if eax.expr.sub(eax.var, c) != ac.expr:
        raise ProofException("∃ I", ac.expr, "premise doesn't match conclusion", ret)
    return ret

##########################################
#
# ∃ x.A(x)  A(c)→ B
# ------------------∃ E
#        B
#
# input eax: a proof of ∃ x. A(x)
# input c: a string with the c to replace
# input ab: a proof of A(c) → B
# input eax: the expression B
# output: a proof for B
#
##########################################
def existsE(eax, c, ab, b):
    ret = step(b, "∃ E", [eax,ab])
    if eax.expr.type() != Node.EXISTS:
        raise ProofException("∃ I", eax.expr, "premise is not in the form ∃  x. A", ret)
    if ab.expr.type() != Node.ARROW:
        raise ProofException("∃ I", ab.expr, "premise is not in the form A[c] →  B", ret)
    if eax.expr.expr.sub(eax.expr.var, c) != ab.expr.lhs:
        raise ProofException("∃ I", eax.expr, "existential and concrete term don't match", ret)
    if ab.expr.rhs != b:
        raise ProofException("∃ I", ab.expr, "premise doesn't match conclusion", ret)
    return ret



#######################################################################################################
# You don't need to look at any of this.
# It's just internals the make the proof checker run.
#######################################################################################################


#######################################3
# These are global variables that
# make the proof checker work correctly.
# Really don't touch these.
#######################################3
premises = []
assumptions = []

# reset the global variables
def clear():
    global premises
    global assumptions
    premises = []
    assumptions = []


# This represents a step in a proof
# each step has an expression (the thing under the bar in the proof rule)
# the rule that was used
# and support (the proofs above the bar)
# While the expr is an expression, the support must all be steps
#
# Note: Since each of the supports is a step, this means that Step in an inductively defined structure.
# That means that Step is really a tree.
# So, our proofs are really trees, even though we're printing them out as a list of steps
class step():
    def __init__(self,expr,rule,support):
        self.expr = expr
        self.rule = rule
        self.support = support
        # used for printing the proof
        self.line = 0
 
    # reset the line numbers for this proof
    def reset(self):
        line = 0
        for s in self.support:
            s.reset()

    def max_assumptions(self):
        l = max([s.max_assumptions() for s in self.support], default=0)
        if self.rule in ["→ I","∀ I"]:
            return 1 + l
        return l

    # prints out a proof
    # first we print what we've actually proven
    # then we do a preorder traversal of the proof tree to print the proof out
    def print_proof(self):
        global premises

        # print out the theorem that was actually proven
        # this might be different than you expect
        print("%s |- %s" % (", ".join([str(p.expr) for p in premises]), self.expr))

        # start the preorder traversal on line 1
        self.print_step(1, 0, self.max_assumptions())

        # Reset ourselfs, so we're consistent
        self.reset()

    def print_step(self, line_no, asms, max_asms):

        # print the children out first
        # since they were earlier steps in the proof
        for s in self.support:
            (line_no,asms) = s.print_step(line_no, asms, max_asms)

        # If we make a new assumption, the put it on the assumption stack
        if self.rule == "assume":
            asms += 1

        # If we are done with an assumption, then remove it from the assumption stack
        if self.rule in ["→ I","∀ I"]:
            asms -= 1

        # set what line we're on
        # this is needed for any later steps
        self.line = line_no

        # print out a bar for each assumption we've made at this point
        for i in range(max_asms):
            if i < asms:
                print("|", end="")
            else:
                print(" ", end="")

        # print the actual step out in the form "line : expr | support"
        print("%5d: %60s | %10s" % (line_no, str(self.expr), self.rule), end = " ")
        print(", ".join([str(s.line) for s in self.support]))
        
        # move onto the next line
        return (line_no + 1, asms)

