class DfaError(Exception):
	pass
	
tokens = []
spaces = 0
def token(tok, lexeme):
	tokens.append((tok,lexeme))

def space():
	global spaces
	spaces += 1
	
def error(c):
	raise DfaError("unknown char \'%s\'" % c)

actions = {
	-1: error,
	0: lambda _: space(),
	3: lambda lexeme: token("FOR", lexeme), 
	6: lambda lexeme: token("NEW", lexeme)
}

# space is a separator, the start state has a transition to itself on " ", and all accepting states have transitions on " " to the start state.
example = {
	(0, " "): 0, 
	(3, " "): 0,
	(6, " "): 0, 
	(0, "f"): 1, (1, "o"): 2, (2, "r"): 3,
	(0, "n"): 4, (4, "e"): 5, (5, "w"): 6
}

F = [3, 6]

while True:
	simulate2(raw_input(), example, 0, F, actions)
	print tokens
	print spaces
	
# in practice, we'll probably be using a parser, the parser needs input tokens as soon as possible (parser and lexical analyser running together), consider the use of a generator.
