import re
from utils import Queue
from tokens import Token, TokenType
		
	
class Scanner:
	
	def run(self, strinput):
		return self.scan(strinput)

	def err(self, tok, lineno, lineoff):
		raise SyntaxError(f'Token "{tok}" not recognized on line {lineno} offset {lineoff}')

	def cache_lineinfo(self, lineno, lineoff):
		i, j = lineno, lineoff
		def get_lineinfo():
			return i, j
		return get_lineinfo
		
	def scan(self, strinput):
		tokens = Queue()
		lineno, lineoff = 0, 0
		while lineoff < len(strinput):
			tok = strinput[lineoff]
			get_lineinfo = self.cache_lineinfo(lineno, lineoff)
			if bool(re.search(r'["\']', tok)):
				closing_quote = tok
				lineoff += 1
				string = strinput[lineoff]
				lineoff += 1
				while not bool(re.search(r'[{}]'.format(closing_quote), strinput[lineoff])):
					string += strinput[lineoff]
					lineoff += 1
				lineoff += 1
				tokens.enqueue(Token(TokenType.CONST, string, get_lineinfo()))
			elif bool(re.search(r'[0-9]', tok)) or tok == '-':
				number = tok
				lineoff += 1
				if tok == '-' and lineoff < len(strinput):
					number += strinput[lineoff]
					lineoff += 1
					if number == '->':
						tokens.enqueue(Token(TokenType.ARROW, number, get_lineinfo()))
						continue
				while lineoff < len(strinput) and (strinput[lineoff] == '.' or bool(re.search(r'[0-9]', strinput[lineoff]))):
					number += strinput[lineoff]
					lineoff += 1
				tokens.enqueue(Token(TokenType.CONST, number, get_lineinfo()))
			elif bool(re.search(r'[a-zA-Z_]', tok)):
				name = tok
				lineoff += 1
				while lineoff < len(strinput) and bool(re.search(r'[a-zA-Z_]', strinput[lineoff])):
					name += strinput[lineoff]
					lineoff += 1
				if name == 'TRUE':
					tokens.enqueue(Token(TokenType.TRUE, name, get_lineinfo()))
				elif name == 'FALSE':
					tokens.enqueue(Token(TokenType.FALSE, name, get_lineinfo()))
				elif name == 'AND':
					tokens.enqueue(Token(TokenType.AND, name, get_lineinfo()))
				elif name == 'OR':
					tokens.enqueue(Token(TokenType.OR, name, get_lineinfo()))
				elif name == 'NOT':
					tokens.enqueue(Token(TokenType.NOT, name, get_lineinfo()))
				elif name == 'return':
					tokens.enqueue(Token(TokenType.RETURN, name, get_lineinfo()))
				elif name == 'func':
					tokens.enqueue(Token(TokenType.FUNC, name, get_lineinfo()))
				else:
					tokens.enqueue(Token(TokenType.IDENT, name, get_lineinfo()))
			elif bool(re.search(r'\s', tok)):
				lineoff += 1
				continue
			elif bool(re.search(r'[-+*/%]', tok)):
				if tok == '+':
					tokentype = TokenType.PLUS
				elif tok == '-':
					tokentype = TokenType.MINUS
				elif tok == '/':
					tokentype = TokenType.DIV
				elif tok == '*':
					tokentype = TokenType.MULT
				elif tok == '%':
					tokentype = TokenType.MOD
				tokens.enqueue(Token(tokentype, tok, get_lineinfo()))
				lineoff += 1
			elif bool(re.search(r'[<>=]', tok)):
				comp = tok
				lineoff += 1
				while lineoff < len(strinput) and bool(re.search(r'[<>=]', strinput[lineoff])):
					comp += strinput[lineoff]
					lineoff += 1
				if comp == '<':
					tokentype = TokenType.LT
				elif comp == '>':
					tokentype = TokenType.GT
				elif comp == '<=':
					tokentype = TokenType.LTE
				elif comp == '>=':
					tokentype = TokenType.GTE
				elif comp == '=':
					tokentype = TokenType.EQ
				elif comp == '<>':
					tokentype = TokenType.NE
				tokens.enqueue(Token(tokentype, comp, get_lineinfo()))
			elif tok == '(':
				tokens.enqueue(Token(TokenType.OPEN_PAREN, tok, get_lineinfo()))
				lineoff += 1
			elif tok == ')':
				tokens.enqueue(Token(TokenType.CLOSED_PAREN, tok, get_lineinfo()))
				lineoff += 1
			elif bool(re.search(r':', tok)):
				lineoff += 1
				if strinput[lineoff] == ':':
					lineoff += 1
					if strinput[lineoff] == '=':
						lineoff += 1
						tokens.enqueue(Token(TokenType.STORE, '::=', get_lineinfo()))
						continue
				self.err(tok, lineno, lineoff)
			elif tok == '{':
				obj = tok
				lineoff += 1
				obj += strinput[lineoff]
				if strinput[lineoff] == '}':
					tokens.enqueue(Token(TokenType.EMPTY, obj, get_lineinfo()))
					lineoff += 1
				else:
					tokens.enqueue(Token(TokenType.OPEN_BRACE, tok, get_lineinfo()))
			elif tok == '}':
				tokens.enqueue(Token(TokenType.CLOSED_BRACE, tok, get_lineinfo()))
				lineoff += 1
			elif tok == ',':
				tokens.enqueue(Token(TokenType.COMMA, tok, get_lineinfo()))
				lineoff += 1
			elif tok == '\n':
				lineno += 1
			else:
				self.err(tok, lineno, lineoff)
		print(tokens)
		return tokens
