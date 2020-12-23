from decimal import Decimal
from abc import ABC, abstractmethod


class Token:
	
	def __init__(self, type, value, lineinfo):
		self.type = type
		self.value = value
		self.lineinfo = lineinfo # tuple (lineno, lineoff)
		
	def __str__(self):
		data = self.type, self.value, self.lineinfo
		return str(data)


class ASTNode(ABC):

	@abstractmethod
	def accept(self, visitor):
		raise NotImplementedError(
			f'Please implement the "accept" method to accept a visitor for the "{self.__class__.__name__}" node'
		)

class AST(ASTNode):
	def __init__(self):
		self.branches = []

	def add_node(self, node):
		self.branches.append(node)

	def get_nodes(self):
		return self.branches

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


class String(ASTNode):
	def __init__(self, value):
		self.value = str(value[1:-1])

	def accept(self, visitor):
		return visitor.visit_String(self)


class Boolean(ASTNode):
	def __init__(self, value):
		self.value = True if value == 'TRUE' else False

	def accept(self, visitor):
		return visitor.visit_Boolean(self)


class Empty(ASTNode):
	def __init__(self):
		self.value = None

	def accept(self, visitor):
		return visitor.visit_Empty(self)


class Context:
	LOAD = 1
	STORE = 2
