from decimal import Decimal
from abc import ABC, abstractmethod

class Token:
	
	def __init__(self, type, value, lineno, lineoff):
		self.type = type
		self.value = value
		self.lineno = lineno
		self.lineoff = lineoff
		
	def __str__(self):
		data = self.type, self.value, self.lineno, self.lineoff
		return str(data)


class ASTNode(ABC):

	@abstractmethod
	def accept(self, visitor):
		raise NotImplementedError(
			f'Please implement the "accept" method to accept a visitor for the "{self.__class__.__name__}" node'
		)

class AST(ASTNode):
	def __init__(self):
		self.tree = []

	def add_node(self, node):
		self.tree.append(node)

	def get_nodes(self):
		return self.tree

	def accept(self, visitor):
		return visitor.visit_AST(self)


class Expr(ASTNode):
	def __init__(self, value):
		self.value = value

	def accept(self, visitor):
		return visitor.visit_Expr(self)


class BinOp(ASTNode):
	def __init__(self, left, op, right):
		self.left = left
		self.op = op
		self.right = right

	def accept(self, visitor):
		return visitor.visit_BinOp(self)

class Number(ASTNode):
	def __init__(self, value):
		self.value = Decimal(value)

	def accept(self, visitor):
		return visitor.visit_Number(self)
