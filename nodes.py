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


class Stmt(ASTNode):

	def __init__(self, value):
		self.value = value
	
	def accept(self, visitor):
		return visitor.visit_Stmt(self)


class Stmts(ASTNode):

	def __init__(self, value):
		self.value = value
	
	def accept(self, visitor):
		return visitor.visit_Stmts(self)


class SingularStmt(ASTNode):

	def __init__(self, value):
		self.value = value
	
	def accept(self, visitor):
		return visitor.visit_SingularStmt(self)


class Assign(ASTNode):

	def __init__(self, target, value):
		self.target = target
		self.value = value
	
	def accept(self, visitor):
		return visitor.visit_Assign(self)


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


class Name(ASTNode):
	def __init__(self, ident, context):
		self.ident = ident
		self.context = context

	def accept(self, visitor):
		return visitor.visit_Name(self)


class Number(ASTNode):
	def __init__(self, value):
		self.value = Decimal(value)

	def accept(self, visitor):
		return visitor.visit_Number(self)


class Context:
	LOAD = 1
	STORE = 2
