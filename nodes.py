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
	def __init__(self):
		self.tree = []

	def add_node(self, node):
		self.tree.append(node)

	def get_nodes(self):
		return self.tree


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
