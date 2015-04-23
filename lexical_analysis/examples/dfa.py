# construct an NFA and by subset construction an equivalent DFA, simulate by this approach:

def simulate(inputs, dfa, start, accepting):
  s = start
  for c in inputs:
    try:
      s = dfa[s,c]
    except KeyError:
    	return False
  if s in accepting:
    return True
  return False

# Dictionary in the form (state, input_symbol) = next_state
example = {(0, "A"): 0, (0, "B"): 1}

# A list of accepting states
F = [1]

simulate("AAAB", example, 0, F) # True
simulate("AAAABx", example, 0, F) # False
