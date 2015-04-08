def create_nfa(states, accepting):
	nfa = {}
	for s in states:
		# (sym, from, to)
		for a in s[0]:
			l = [] # to handle collisions
			l.extend(s[2])
			if (a, s[1]) in nfa:
				for e in l:
					if not e in nfa[(a, s[1])]: nfa[(a, s[1])].append(e)
			else:
				nfa[(a, s[1])] = l
	return nfa, accepting

def match(inpt, nfa):
	states = [0]
	for i in inpt:
		next = []
		for s in states: 
			if (i,s) in nfa[0]:
				next.extend(nfa[0][i, s])
		states = next
	if [e for e in states if e in nfa[1]]:
		return True

nfa = create_nfa([
	(["a", "b"], 0, [0]),
	(["b"], 0, [1]),
	(["b"], 1, [2]),
	(["b"], 2, [3]),
], [3])

match("abbb", nfa) # True
