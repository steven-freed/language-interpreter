import re
from utils import Queue
from nodes import Token
		
	
class Scanner:
	
	def run(self, strinput):
		return self.scan(strinput)
		
	def scan(self, strinput):
		tokens = Queue()
		lineno, lineoff = 0, 0
		while lineoff < len(strinput):
			tok = strinput[lineoff]
			if bool(re.search(r'[0-9]', tok)):
				number = tok
				lineoff += 1
				while lineoff < len(strinput) and (strinput[lineoff] == '.' or bool(re.search(r'[0-9]', strinput[lineoff]))):
					number += strinput[lineoff]
					lineoff += 1
				tokens.enqueue(Token('const', number, lineno, lineoff))
			elif bool(re.search(r'[a-zA-Z]', tok)):
				name = tok
				lineoff += 1
				while lineoff < len(strinput) and bool(re.search(r'[a-zA-Z]', strinput[lineoff])):
					name += strinput[lineoff]
					lineoff += 1
				tokens.enqueue(Token('id', name, lineno, lineoff))
			elif bool(re.search(r'\s', tok)):
				lineoff += 1
				continue
			elif bool(re.search(r'[+-/*%]', tok)):
				tokens.enqueue(Token('op', tok, lineno, lineoff))
				lineoff += 1
			elif bool(re.search(r'[()]', tok)):
				tokens.enqueue(Token('paren', tok, lineno, lineoff))
				lineoff += 1
			elif bool(re.search(r':', tok)):
				lineoff += 1
				while lineoff < len(strinput) and bool(re.search(r'(:|=)', strinput[lineoff])):
					tok += strinput[lineoff]
					lineoff += 1
				tokens.enqueue(Token('store', tok, lineno, lineoff))
			elif tok == '\n':
				lineno += 1
			else:
				raise SyntaxError(f'Token "{tok}" not recognized on line {lineno} offset {lineoff}')
		return tokens
	
