import re
from utils import Queue
from nodes import Token
		
	
class Scanner:
	
	def run(self, strinput):
		return self.scan(strinput)

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
				string = tok
				closing_quote = tok
				lineoff += 1
				while not bool(re.search(r'[{}]'.format(closing_quote), strinput[lineoff])):
					string += strinput[lineoff]
					lineoff += 1
				string += strinput[lineoff]
				lineoff += 1
				tokens.enqueue(Token('const', string, get_lineinfo()))
			elif bool(re.search(r'[0-9]', tok)) or tok == '-':
				number = tok
				lineoff += 1
				while lineoff < len(strinput) and (strinput[lineoff] == '.' or bool(re.search(r'[0-9]', strinput[lineoff]))):
					number += strinput[lineoff]
					lineoff += 1
				tokens.enqueue(Token('const', number, get_lineinfo()))
			elif bool(re.search(r'[a-zA-Z_]', tok)):
				name = tok
				lineoff += 1
				while lineoff < len(strinput) and bool(re.search(r'[a-zA-Z_]', strinput[lineoff])):
					name += strinput[lineoff]
					lineoff += 1
				if name == 'TRUE' or name == 'FALSE':
					tokens.enqueue(Token('const', name, get_lineinfo()))
				elif name == 'AND' or name == 'OR':
					tokens.enqueue(Token('op', name, get_lineinfo()))
				else:
					tokens.enqueue(Token('id', name, get_lineinfo()))
			elif bool(re.search(r'\s', tok)):
				lineoff += 1
				continue
			elif bool(re.search(r'[+-/*%]', tok)):
				tokens.enqueue(Token('op', tok, get_lineinfo()))
				lineoff += 1
			elif bool(re.search(r'[()]', tok)):
				tokens.enqueue(Token('paren', tok, get_lineinfo()))
				lineoff += 1
			elif bool(re.search(r':', tok)):
				lineoff += 1
				expected = ':'
				while lineoff < len(strinput) and bool(re.search(r'({})'.format(expected), strinput[lineoff])):
					tok += strinput[lineoff]
					lineoff += 1
					expected = '='
				tokens.enqueue(Token('store', tok, get_lineinfo()))
			elif tok == '{':
				obj = tok
				lineoff += 1
				obj += strinput[lineoff]
				if strinput[lineoff] == '}':
					tokens.enqueue(Token('const', obj, get_lineinfo()))
					lineoff += 1
			elif tok == '\n':
				lineno += 1
			else:
				print(tokens)
				raise SyntaxError(f'Token "{tok}" not recognized on line {lineno} offset {lineoff}')
		return tokens
