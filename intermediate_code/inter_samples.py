from parsing.grammar import *

def get_sample():
    return Grammar([
        NonTerminal("S'", [
            "S ';'"
        ]),
        # arithmetic
        NonTerminal("S", [
            "'id' '=' E"
        ]),
        NonTerminal('E', [
            "E '+' T",
            "E '-' T",
            "T"
        ]),
        NonTerminal('T', [
            "T '*' F",
            "T '/' F",
            "F"
        ]),
        NonTerminal('F', [
            "'(' E ')'",
            "'id'"
        ]),
        # relational
        NonTerminal("S'", [
            "'id' '<' 'id'",
            "'id' '<=' 'id'",
            "'id' '>' 'id'",
            "'id' '>=' 'id'",
            "'id' '==' 'id'",
            "'id' '<>' 'id'",
        ]),
        #conditional
        NonTerminal("S", [
            "C"
        ]),
        NonTerminal("C", [
            "'if' '(' R ')' 'then' S",
            "'if' '(' R ')' 'then' S 'else' S",
        ]),
    ])

















