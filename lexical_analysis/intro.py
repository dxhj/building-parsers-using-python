
"""
What's lexical analysis? 
  The first phase is called lexical analysis or scanning. The lexical analyzer reads the stream of characters making up the source program
and groups the characters into meaningful sequences called lexemes. - Dragon's Book.

  Well, there are so many ways to tokenize things out in Python, using the version of Lex-Yacc to Python (http://www.dabeaz.com/ply/), 
simulating a NFA (user xysun wrote a beautiful implementation of Thompson's algorithm: https://github.com/xysun/regex), the re module (here's the trick: http://effbot.org/zone/xml-scanner.htm), 
or writing by hand.
"""

# A simple example by hand (regex for identifiers -> [a-zA-Z][a-zA-Z0-9]*):
if char.isalpha(): # [a-zA-Z]
	sbuffer = []
	while char.isalpha() or char.isdigit(): # [a-zA-Z0-9]*
		sbuffer.append(char)
		char = nextchar()
	return Word("".join(sbuffer), ID) # Word<VALUE, ID>

# [0-9]+
if char.isdigit(): # [0-9]
	num = 0
	while char.isdigit(): # [0-9]+
		num = num * 10 + int(char)
		char = nextchar()
	return Num(num, INT) # Num<VALUE, INT>

# This way can be simple and doesn't need any module, but how grows the necessity to tokenize more kind of tokens it can be troublesome.
# In the next tutorial we're going to study it.

