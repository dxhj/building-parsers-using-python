def simulate2(input, dfa, start, accepting, actions):
	s = start
	sbuffer = []
	for c in input:
		sbuffer.append(c)
		try:
			s = dfa[s,c]
			try:
				actions[s]("".join(sbuffer))
				sbuffer = []
			except KeyError:
				pass # no action
		except KeyError:
			actions[-1](c)
	if s in accepting:
		return True
	return False

# usage: simulate2_example.py
