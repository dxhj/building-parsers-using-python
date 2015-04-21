# This is surely not the best implementation. (hahaha)
# Supports: Kleene star, plus rep., dot, character classes (just ranges like [a-z], [a-zA-Z]), alternation, and concatenation. 

from collections import namedtuple

class State(object):
	def __init__(self):
		self.e_transitions = []
		self.transitions = {}
		self.acceptance = True

class NFA(object):
	def __init__(self, start, end):
		self.start = start
		self.end = end
		start.acceptance = False

	def e_closure(self, s, states):
		if s in states:
			return
		states.append(s)
		for e in s.e_transitions:
			self.e_closure(e, states)

	def accepts(self, inpt):
		states = []
		self.e_closure(self.start, states)
		for ch in inpt:
			next_states = []
			for state in states:
				if ch in state.transitions:
					self.e_closure(state.transitions[ch], next_states)
				elif "RANGE" in state.transitions:
					ord_c = ord(ch)
					if ord_c <= state.transitions["RANGE"][1][0] or ord_c <= state.transitions["RANGE"][1][1]:
						self.e_closure(state.transitions["RANGE"][0], next_states)
				elif "." in state.transitions:
					self.e_closure(state.transitions["."], next_states)
			states = next_states
		for state in states:
			if state.acceptance:
				return True
		return False

class Parser(object):
	def __init__(self, inpt):
		self.Token = namedtuple("Token", "type lexeme")
		self.lookahead = self.tokenize(inpt)
		self.current = self.lookahead.next()
		self.tokens = []
		self.exp()

	def tokenize(self, inpt):
		s = {"|": "ALT", "*": "KLEENE", "+": "PLUS", "?": "QUESTION", "(": "LEFTP", ")": "RIGHTP", "[": "LEFTB", "]": "RIGHTB", "-": "SEP"}
		for e in inpt:
			if e in s:
				yield self.Token(s[e], e)
			else:
				yield self.Token("CHAR", e)
		yield self.Token("NONE", "")

	def consume(self, tok):
		if self.current.type == tok:
			t = self.current
			self.current = self.lookahead.next()
			return t
		else:
			raise SyntaxError

	def exp(self):
		self.term()
		if self.current.type == "ALT":
			t = self.consume("ALT")
			self.exp()
			self.tokens.append(t)

	def term(self):
		self.factor()
		if not self.current.lexeme in ")|":		
			self.term()
			self.tokens.append(self.Token("CONCAT", "."))

	def factor(self):
		self.last()
		if self.current.type in ["KLEENE", "PLUS", "QUESTION"]:
			self.tokens.append(self.consume(self.current.type))

	def option(self, l):
		t0 = ord(self.consume("CHAR").lexeme)
		self.consume("SEP")
		t1 = ord(self.consume("CHAR").lexeme)
		if t0 > t1:
			raise ValueError("character classes must be in the form [MIN_CHAR-MAX_CHAR]")
		if l:
			if t0 < l[0]: l[0] = t0
			if t1 > l[1]: l[1] = t1
		else:
			l.extend([t0, t1])
		if self.current.type == "CHAR":
			return self.option(l)
		return l


	def last(self):
		if self.current.type == "LEFTP":
			self.consume("LEFTP")
			self.exp()
			self.consume("RIGHTP")
		elif self.current.type == "CHAR":
			self.tokens.append(self.consume("CHAR"))
		if self.current.type == "LEFTB":
			self.consume("LEFTB")
			self.tokens.append(self.Token("RANGE", self.option([])))
			self.consume("RIGHTB")

def create_nfa(r):
	stack = []
	for t in Parser(r).tokens:
		if t.type in ["CHAR", "RANGE"]:
			s0 = State()
			s1 = State()
			if t.type == "RANGE":
				s0.transitions["RANGE"] = (s1, t.lexeme)
			else:
				s0.transitions[t.lexeme] = s1
			stack.append(NFA(s0, s1))
		elif t.type == "CONCAT":
			n2 = stack.pop()
			n1 = stack.pop()
			n1.end.e_transitions.append(n2.start)
			n1.end.acceptance = False
			stack.append(NFA(n1.start, n2.end))
		elif t.type == "ALT":
			n2 = stack.pop()
			n1 = stack.pop()
			s0 = State()
			s0.e_transitions.extend([n1.start, n2.start])
			s1 = State()
			n1.end.e_transitions.append(s1)
			n2.end.e_transitions.append(s1)
			stack.append(NFA(s0, s1))
		elif t.type in ["KLEENE", "PLUS"]:
			s0 = State()
			s1 = State()
			n1 = stack.pop()
			s0.e_transitions.append(n1.start)
			if t.type == "KLEENE":
				s0.e_transitions.append(s1)
			n1.end.e_transitions.extend([n1.start, s1])
			n1.end.acceptance = False
			stack.append(NFA(s0, s1))
		elif t.type in ["QUESTION"]:
			n1 = stack.pop()
			n1.start.e_transitions.append(n1.end)
			stack.append(n1)
	return stack.pop()
