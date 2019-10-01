
# proofs: representing proofs in propositional logic

Building on last time, now we move on to representing proofs in propositional logic.

You can run this with 
> python3 main.py

Now, the proofs will be written in Main.py
See Main.py for an example.

This program will support the following expressions
* a && b - And
* a || b - Or
* a -> b - Implication
* ~a     - Not
* T      - True
* F      - False
* v      - variable

We support following proof rules.
from Proof import (clear
*  premise  - Add a premise
*  assume   - Make an assumption
*  assumed  - Use a previously made assumption
*  andI     - And Introduction
*  andEL    - And elimination on the left
*  andER    - And elimination on the right
*  orIL     - Or introduction on the left 
*  orIR     - Or introduction on the right
*  orE      - Or elimination
*  arrowI   - Arrow introduction
*  arrowE   - Arrow elimination
*  notI     - Not Introduction
*  notE     - Not elimination (contradiction)
*  TI       - True introduction
*  FE       - False elmination
*  LEM      - Law of the Excluded Middle

We've added a few files
* Proof.py File contianing the proof checking rules.
* Match.py a file for helping with pattern matching.
* AST.py The Abstract syntax tree representing boolean expression
* Parser.py a file for parsing boolean expressions for the command line
* Exceptions.py a file containing the verious exceptions
* Main.py A simple program to read a single command line argument

This time We're only concerned about Proofs, Main, and AST
