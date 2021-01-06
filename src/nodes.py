from decimal import Decimal
from abc import ABC, abstractmethod
import operator


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

	def __repr__(self):
		return f'<target={self.target}, value={self.value}>'


class Expr(ASTNode):
	def __init__(self, value):
		self.value = value

	def accept(self, visitor):
		return visitor.visit_Expr(self)

	def __repr__(self):
		return f'<value={self.value}>'


class BinOp(ASTNode):

	OP_MAP = {
		'+': operator.add, '-': operator.sub,
		'*': operator.mul, '/': operator.truediv,
		'%': operator.mod
	}

	def __init__(self, left, op, right):
		self.left = left
		self.op = op
		self.right = right

	def accept(self, visitor):
		return visitor.visit_BinOp(self)

	def __repr__(self):
		return f'<left={self.left}, op={self.op}, right={self.right}>'


class Compare(ASTNode):

	OP_MAP = {
		'=': operator.eq, '<>': operator.ne,
		'<': operator.lt, '>': operator.gt,
		'<=': operator.le, '>=': operator.ge
	}

	def __init__(self, ops, comparators):
		self.ops = ops
		self.comparators = comparators

	def accept(self, visitor):
		return visitor.visit_Compare(self)

	def __repr__(self):
		return f'<ops={self.ops}, comparators={self.comparators}>'


class BoolOp(ASTNode):

	OP_MAP = {
		'OR': lambda a,b: a or b, 'AND': lambda a,b: a and b
	}

	def __init__(self, op, values):
		self.op = op
		self.values = values

	def accept(self, visitor):
		return visitor.visit_BoolOp(self)

	def __repr__(self):
		return f'<op={self.op}, values={self.values}>'


class Arg(ASTNode):
	def __init__(self, ident, default=None):
		self.ident = ident
		self.default = default
	
	def accept(self, visitor):
		return visitor.visit_Arg(self)

	def __str__(self):
		return f'<ident={self.ident}, default={self.default}>'


class Return(ASTNode):
	def __init__(self, value=None):
		self.value = value
	
	def accept(self, visitor):
		return visitor.visit_Return(self)

	def __repr__(self):
		return f'<value={self.value}>'


class FunctionDec(ASTNode):
	def __init__(self, ident, args, body, lambda_=False):
		self.ident = ident
		self.args = args or []
		self.body = body or []
		self.lambda_ = lambda_

	def accept(self, visitor):
		return visitor.visit_FunctionDec(self)

	def __repr__(self):
		return f'<ident={self.ident}, args={self.args}, body={self.body}, lambda={self.lambda_}>'


class FunctionCall(ASTNode):
	def __init__(self, ident, args):
		self.ident = ident
		self.args = args or []

	def accept(self, visitor):
		return visitor.visit_FunctionCall(self)

	def __repr__(self):
		return f'<ident={self.ident}, args={self.args}>'


class Name(ASTNode):
	def __init__(self, ident, context):
		self.ident = ident
		self.context = context

	def accept(self, visitor):
		return visitor.visit_Name(self)

	def __repr__(self):
		return f'<ident={self.ident}, context={self.context}>'


class Number(ASTNode):
	def __init__(self, value):
		self.value = Decimal(value)

	def accept(self, visitor):
		return visitor.visit_Number(self)

	def __str__(self):
		return str(self.value)

	def __repr__(self):
		return f'<value={self.value}>'


class String(ASTNode):
	def __init__(self, value):
		self.value = value

	def accept(self, visitor):
		return visitor.visit_String(self)

	def __str__(self):
		return '"' + str(self.value) + '"'

	def __repr__(self):
		return f'<value={self.value}>'


class Boolean(ASTNode):

	TRUE = 'TRUE'
	FALSE = 'FALSE'

	def __init__(self, value):
		if value in (True, self.TRUE):
			self.value = True
		else:
			self.value = False

	def accept(self, visitor):
		return visitor.visit_Boolean(self)

	def __str__(self):
		if self.value:
			return self.TRUE
		else:
			return self.FALSE

	def __repr__(self):
		return f'<value={str(self)}>'


class Inverse(ASTNode):
	def __init__(self, value):
		self.value = value

	def accept(self, visitor):
		return visitor.visit_Inverse(self)

	def __str__(self):
		if self.value:
			return Boolean.TRUE
		else:
			return Boolean.FALSE

	def __repr__(self):
		return f'<value={str(self)}>'


class Empty(ASTNode):
	def __init__(self, value=None):
		self.value = value

	def accept(self, visitor):
		return visitor.visit_Empty(self)

	def __str__(self):
		return "{}"

	def __repr__(self):
		return f'<value={str(self)}>'


class Context:
	LOAD = 1
	STORE = 2
