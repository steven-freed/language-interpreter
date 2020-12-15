import re
from astnodes import Token
from pprint import pprint


class Queue:
	
	def __init__(self, collection=[]):
		self.q = collection
		
	def enqueue(self, node):
		self.q.append(node)
		
	def dequeue(self):
		try:
			return self.q.pop(0)
		except IndexError:
			return None
		
	def peek(self):
		try:
			return self.q[0]
		except IndexError:
			return None
	
	def __len__(self):
		return len(self.q)
		
	def __str__(self):
		return str([str(i) for i in self.q])
		
	
class Scanner:
	
	def run(self, strinput):
		return self.__scan__(strinput)
		
	def __scan__(self, strinput):
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
			elif tok == '\n':
				lineno += 1
			else:
				raise SyntaxError(f'Token {too} not recognized on line {lineno} offset {lineoff}')
		return tokens
	
