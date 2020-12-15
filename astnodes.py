from decimal import Decimal

class Token:
	
	def __init__(self, type, value, lineno, lineoff):
		self.type = type
		self.value = value
		self.lineno = lineno
		self.lineoff = lineoff
		
	def __str__(self):
		data = self.type, self.value, self.lineno, self.lineoff
		return str(data)


class AST:
	
	def __init__(self, module):
		self.module = module
	
			
class Module:
	
	def __init__(self, body=[]):
		self.body = body
		

class Expr:
	
	def __init__(self, value):
		self.value = value


class BinOp:
	
	def __init__(self, left, op, right):
		self.left = left
		self.op = op
		self.right = right

class Number:
	
	def __init__(self, value):
		self.value = Decimal(value)
