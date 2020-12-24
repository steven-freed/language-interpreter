from decimal import Decimal
from abc import ABC, abstractmethod
from enum import Enum


class Token:
	
	def __init__(self, type, value, lineinfo):
		self.type = type
		self.value = value
		self.lineinfo = lineinfo # tuple (lineno, lineoff)
		
	def __str__(self):
		data = self.type, self.value, self.lineinfo
		return str(data)


class Visitor(ABC):

	@abstractmethod
	def visit_AST(self, ast):
		raise NotImplementedError(f'Please implement the visitor method for AST')

	@abstractmethod
	def visit_Expr(self, expr):
		raise NotImplementedError(f'Please implement the visitor method for Expr')

	@abstractmethod
	def visit_Assign(self, assign):
		raise NotImplementedError(f'Please implement the visitor method for Assign')
		
	@abstractmethod
	def visit_BinOp(self, binop):
		raise NotImplementedError(f'Please implement the visitor method for BinOp')
		
	@abstractmethod
	def visit_Number(self, number):
		raise NotImplementedError(f'Please implement the visitor method for Number')

	@abstractmethod
	def visit_String(self, string):
		raise NotImplementedError(f'Please implement the visitor method for String')

	@abstractmethod
	def visit_Empty(self, empty):
		raise NotImplementedError(f'Please implement the visitor method for Empty')


class ASTNode(ABC):

	@abstractmethod
	def accept(self, visitor):
		raise NotImplementedError(
			f'Please implement the "accept" method to accept a visitor for the "{self.__class__.__name__}" node'
		)

class AST(ASTNode):
	def __init__(self):
		self.branches = []

	def add_branch(self, node):
		self.branches.append(node)

	def accept(self, visitor):
		return visitor.visit_AST(self)


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


class Compare(ASTNode):
	def __init__(self, ops, comparators):
		self.ops = ops
		self.comparators = comparators

	def accept(self, visitor):
		return visitor.visit_Compare(self)


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
		self.value = True if value in (True, 'TRUE') else False

	def accept(self, visitor):
		return visitor.visit_Boolean(self)

	def __repr__(self):
		return 'TRUE' if self.value else 'FALSE'


class Empty(ASTNode):
	def __init__(self):
		self.value = None

	def accept(self, visitor):
		return visitor.visit_Empty(self)


class Context:
	LOAD = 1
	STORE = 2
