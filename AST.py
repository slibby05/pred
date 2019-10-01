from enum import Enum
from Exceptions import SubException

############################################################################################
# These classes represent the different types of propositional logic expressions.
# 
# Remember each expression can be represented as a Tree.
# So (a || b) && ~c is really the tree:
#        &&
#       /  \
#      /    \
#     ||     ~
#    /  \    |
#   /    \   c
#  a      b   
#
# We can construct this tree in python with:
# And(Or(Var("a"), Var("b")), Not(Var("c")))
#
# Since variables make this code harder to read
# for the rest of this file I'll use the variables
# a = Var("a")
# b = Var("b")
# c = Var("c")
# Now the above expression can be rewritten as
# And(Or(a,b), Not(c))
############################################################################################

# This tells us what type of Node we've created
# You don't need to worry about this part.
class Node(Enum):
    ARROW  = 1
    OR     = 2
    AND    = 3
    NOT    = 4
    VAR    = 5
    LIT    = 6
    PRED   = 7
    FORALL = 8
    EXISTS = 9

############################################################################################
# An And node represents the expression a && b
# Each and node has a 
# 1. left hand side (lhs)
# 2. right hand side (rhs)
#
# In this case the lhs = "a", and the rhs = "b"
#
# The And node (along with every other type of expression)
# has several methods that we can call
#
# __init__() is the constructor, this is what is called when we write And(a,b)
#
# __str__()  returns a string representing the expression (this is what str() calls)
# example:
#  str(And(a,b)) returns the string "(a && b)"
#
# __eq__()   returns a True if both expressions are identical (this is what a == b calls)
# example:
#  And(a,b) == And(b,a) returns False.
#  Even though these two expressions are equivalent,
#  they are not literally the same expression.
#
# vars()     returns the set of all variables is the expression
# Example:
#  And(a,b).vars() returns {"a","b"}
#
# type()     returns the type of the node (this isn't used)
# Example:
#  And(a,b).type() returns Node.AND
#
# sub()      return a copy of the expresioin with x substituted for c
# Example:
#  And(P(x,y),Forall(x,Q(x,y))).sub("x", "c") returns And(P(c,y),Forall(x,Q(x,y)))
#  Although we are substituting x for c, we don't replace the x in Q, 
#  because it's under a Forall(x,...)
#
############################################################################################
class And():
    def __init__(self, l, r):
        self.lhs = l
        self.rhs = r

    def __str__(self):
        return "(" + str(self.lhs) + " ∧ " + str(self.rhs) + ")"

    def __eq__(self, other):
        return self.type() == other.type() and \
                self.lhs == other.lhs and \
                self.rhs == other.rhs

    def sub(self, x, v):
        raise SubException("And")

    def type(self):
        return Node.AND

############################################################################################
# An Or node represents the expression a || b
# We can construct one with Or(a,b)
# 
# You'll notice that this is very similar to the And node
############################################################################################
class Or():
    def __init__(self, l, r):
        self.lhs = l
        self.rhs = r

    def __str__(self):
        return "(" + str(self.lhs) + " ∨ " + str(self.rhs) + ")"

    def __eq__(self, other):
        return self.type() == other.type() and \
                self.lhs == other.lhs and \
                self.rhs == other.rhs

    def sub(self, x, v):
        raise SubException("Or")

    def type(self):
        return Node.OR

############################################################################################
# An Arrow node represents the expression a -> B
# We can construct one with Arrow(a,b)
# 
# You'll notice that this is very similar to the And node
############################################################################################
class Arrow():
    def __init__(self, l, r):
        self.lhs = l
        self.rhs = r

    def __str__(self):
        return "(" + str(self.lhs) + " → " + str(self.rhs) + ")"

    def __eq__(self, other):
        return self.type() == other.type() and \
                self.lhs == other.lhs and \
                self.rhs == other.rhs

    def sub(self, x, v):
        raise SubException("Arrow")

    def type(self):
        return Node.ARROW

############################################################################################
# A Not node represents the expression ~a
# We can construct one with Not(a)
# 
# This is different from the And node in that it only has 1 child the lhs
############################################################################################
class Not():
    def __init__(self, l):
        self.lhs = l

    def __str__(self):
        return "(¬ " + str(self.lhs) + ")"

    def __eq__(self, other):
        return self.type() == other.type() and \
                self.lhs == other.lhs

    def sub(self, x, v):
        raise SubException("Not")

    def type(self):
        return Node.NOT



############################################################################################
# A Lit node represents a literal value (T or F)
# We can construct one with true() or false()
# 
# Lit nodes don't have any children, but they do have a value (True or False)
############################################################################################
class Lit():
    def __init__(self, val):
        self.val = val

    def __str__(self):
        if self.val:
            return "T"
        else:
            return "⊥ "

    def __eq__(self, other):
        return self.type() == other.type() and \
                self.val == other.val

    def sub(self, x, v):
        raise SubException("Lit")

    def type(self):
        return Node.LIT


# these are for convenience
# Don't call Lit(True) directly, just use true()
def true():
    return Lit(True)
def false():
    return Lit(False)

############################################################################################
# A Var node represents a variable
# We can construct one with Var("a")
# The string can be any string we want, but you should maksure it only consists of letter
# also, try to avoid T, F, true, True, False, false
# It won't break anything, but it will look confusing with printing the output.
# 
# Var nodes don't have any children, but they have a name
# to evaluate a Var we need to look it up in the environment.
############################################################################################
class Var:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.type() == other.type() and \
                self.name == other.name


    def sub(self, x, v):
        raise SubException("Var")

    def type(self):
        return Node.VAR

############################################################################################
# A Forall node represents the expression ∀ x. P(x)
# We can construct one with Forall("x", ...)
# Notice that "x" is a string, not a variable.
############################################################################################

class Forall():
    def __init__(self, v, e):
        self.var = v
        self.expr = e

    def __str__(self):
        return "(∀ " + self.var + ". " + str(self.expr) + ")"

    def __eq__(self, other):
        return self.type() == other.type() and \
                self.var == other.var and \
                self.expr == other.expr

    def sub(self, x, v):
        raise SubException("Forall")

    def type(self):
        return Node.FORALL

############################################################################################
# An Exists node is just like a forall node
#
############################################################################################

class Exists():
    def __init__(self, v, e):
        self.var = v
        self.expr = e

    def __str__(self):
        return "(∃ " + self.var + ". " + str(self.expr) + ")"

    def __eq__(self, other):
        return self.type() == other.type() and \
                self.var == other.var and \
                self.expr == other.expr

    def sub(self, x, v):
        raise SubException("Exists")

    def type(self):
        return Node.EXISTS

############################################################################################
# A Pred node represents a predicate
# A predicate must have a name, but it can have any number of arguments.
#
# We store the arguments in a list.
# If we have no arguments then the list is empty.
############################################################################################

class Pred():
    def __init__(self, n, vs):
        self.name = n
        self.vars = vs

    def __str__(self):
        return self.name + "(" + ", ".join(self.vars) + ")"

    def __eq__(self, other):
        return self.type() == other.type() and \
                self.name == other.name and \
                self.vars == other.vars

    def sub(self, x, v):
        raise SubException("Pred")


    def type(self):
        return Node.PRED

