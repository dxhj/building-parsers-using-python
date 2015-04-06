class Env(object):
	def __init__(self, prev):
		self.table = {}
		self.prev = prev 

	def put(self, symbol):
		if symbol.lexeme in self.table:
			raise NameError("variable {} already exists".format(symbol.lexeme))
		self.table[symbol.lexeme] = symbol

	def get(self, idt):
		e = self
		while e is not None:
			if idt in e.table:
				return e.table[idt]
			e = e.prev

class Symbol(object):
	def __init__(self, lexeme, typ, value):
		self.lexeme = lexeme
		self.type = typ
		self.value = value

class BlockParser(object):
	def __init__(self):
		pass

	def token_g(self):
		for i in self.inpt:
			yield i

	def tokenize(self, i): # Ugly function for test purposes (PLY is made for that)
		if i == "int":
			return (i.upper(), i)
		if i == "=":
			return ("ASSIGN", i)
		if i == "{":
			return ("LEFT_BRACE", i)
		if i == "}":
			return ("RIGHT_BRACE", i)
		if i == ";":
			return ("SEMI_COLON", i)    
		if i.isalpha():
			return ("ID", i)
		if i.isdigit():
			return ("NUM", i)
		raise SyntaxError

	def match(self, terminal): # ...
		if self.lookahead[0] == terminal:
			if terminal == "EOL":
				return None
			self.lookahead = self.token.next()
		else:
			raise SyntaxError

	def parse(self, inpt):
		self.inpt = map(self.tokenize, inpt.split()) # I assume you'll be using a good lexical analyzer
		self.inpt.append(("EOL", ""))
		self.token = self.token_g()
		self.lookahead = self.token.next()
		self.top = None
		self.block()
		self.match("EOL")

	def block(self):
		saved = self.top
		print "{",
		self.match("LEFT_BRACE")
		self.top = Env(saved)
		self.block_body()
		self.match("RIGHT_BRACE")
		print "}",
		self.top = saved

	def block_body(self):
		if self.lookahead[0] == "INT": # Declaration 
			self.decl()
			self.block_body()
		elif self.lookahead[0] == "LEFT_BRACE":
			self.block()
			self.block_body()
		elif self.lookahead[0] == "ID":
			self.id()
			self.block_body()

	def decl(self):
		# decl -> type id ASSIGN expr
		self.match("INT") 
		lexeme = self.lookahead[1]
		self.match("ID")
		self.match("ASSIGN")
		value = self.lookahead[1]
		self.match("NUM")
		self.top.put(Symbol(lexeme, "INT", value))
		self.match("SEMI_COLON")

	def id(self):
		# id -> ID
		s = self.top.get(self.lookahead[1])
		if s is None:
			raise NameError("{} is not defined".format(self.lookahead[1]))
		self.match("ID")
		print "(", s.lexeme, ":", s.type, "->", s.value, ")",	

b = BlockParser()

b.parse("{ int a = 2 ; a { int a = 3 ; a } a }") 
# { ( a : INT -> 2 ) { ( a : INT -> 3 ) } ( a : INT -> 2 ) }

b.parse("{ int bx = 344 ; int bxx = 3444 ; { int bx = 0 ; { bxx } bx } bx bxx }")
# { { { ( bxx : INT -> 3444 ) } ( bx : INT -> 0 ) } ( bx : INT -> 344 ) ( bxx : INT -> 3444 ) }

b.parse("{ int a = 1 ; int b = 2 ; int c = 3 ; { a b c } }")
# { { ( a : INT -> 1 ) ( b : INT -> 2 ) ( c : INT -> 3 ) } }

b.parse("{ { int x = 10 ; } int x = 9 ; x }")
# { { } ( x : INT -> 9 ) }

b.parse("{ int x = 12 ; { int x = 1 ; x } { int x = 2 ; x } x }")
# { { ( x : INT -> 1 ) } { ( x : INT -> 2 ) } ( x : INT -> 12 ) }
