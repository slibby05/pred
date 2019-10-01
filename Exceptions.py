
class ParseException(Exception):
    def __init__(self, line, expected, got):
        self.line = line
        self.expected = expected
        self.got = got
    def __str__(self):
        return "Error at %d: expected %s, but got %s" % (self.line, self.expected, self.got)

class LexException(Exception):
    def __init__(self, line, got):
        self.line = line
        self.got = got
    def __str__(self):
        return "Error at %d: invalid symbol %c" % (self.line, self.got)

class SubException(Exception):
    def __init__(self, node):
        self.node = node
    def __str__(self):
        return "Error: sub not implemented for " + self.node

class ProofException(Exception):
    def __init__(self, rule, expr, reason, proof):
        self.rule = rule
        self.expr = expr
        self.reason = reason
        self.proof = proof
    def print(self):
        self.proof.print_proof()
        print("Error: proof rule %s can't be applies to %s, because %s" % (self.rule, str(self.expr), self.reason))
