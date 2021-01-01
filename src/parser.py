from utils import (
	isfloat, log, Stack
)
from tokens import Token, TokenType
from nodes import (
	Number, BinOp, Expr, AST, Context,
	Assign, Name, String, Boolean, Empty, Compare,
	BoolOp, Inverse, FunctionDec, Param, Return
)

		
class Parser:
	
	def run(self, tokens):
		self.callstack = Stack()
		tokenstack = Stack(collection=tokens)
		return self.parse(tokenstack)
	
	def parse(self, tokens):
		tree = AST()
		while len(tokens):
			tree.add_branch(self.stmt(tokens))
		print(tree.branches[0].value)
		return tree
	@log
	def stmt(self, tokens):
		return self.stmts(tokens)
	@log
	def stmts(self, tokens):
		node = self.singular_stmt(tokens)
		if not node:
			node = self.compound_stmt(tokens)
		return node
	@log
	def compound_stmt(self, tokens):
		if self.match(tokens.peek(), (TokenType.IDENT,)):
			node = self.function_dec(tokens)
		return node
	@log
	def function_dec(self, tokens):
		if self.match(tokens.peek(), (TokenType.IDENT,)):
			ident = tokens.pop()
			if self.match(tokens.peek(), (TokenType.OPEN_PAREN,)):
				tokens.pop()
				args = []
				while not self.match(tokens.peek(), (TokenType.CLOSED_PAREN,)):
					arg = self.params(tokens)
					args.append(arg)
				if self.match(tokens.peek(), (TokenType.ARROW,)):
					tokens.pop()
					block = self.block(tokens)
					node = FunctionDec(ident, args, body=block, returns=None)
		return node
	@log
	def block(self, tokens):
		if self.match(tokens.peek(), TokenType.OPEN_BRACE):
			node = self.stmts(tokens)
		else:
			node = self.singular_stmt(tokens)
		return node
	@log
	def params(self, tokens):
		param = self.param(tokens)
		Param(param, default=self.param_default(tokens))
	@log
	def param_default(self, tokens):
		default = None
		if self.match(tokens.peek(), (TokenType.EQ,)):
			tokens.pop()
			default = self.expr(tokens)
		return node
	@log
	def param(self, tokens):
		name = self.atom(tokens)
		return name
	@log
	def singular_stmt(self, tokens):
		node = self.expr(tokens)
		if isinstance(node.value, Name) and self.match(tokens.peek(), (TokenType.STORE,)):
			tokens.push(self.callstack.pop())
			node = self.assign(tokens)
		elif self.match(tokens.peek(), (TokenType.RETURN,)):
			tokens.pop()
			node = self.return_stmt(tokens)
		return node
	@log
	def return_stmt(self, tokens):
		expr = self.expr(tokens)
		return Return(expr)

	def assign(self, tokens):
		name = self.atom(tokens)
		tokens.pop()
		value = self.expr(tokens)
		return Assign(name, value)
	@log
	def expr(self, tokens):
		return Expr(self.disjunction(tokens))
	@log
	def disjunction(self, tokens):
		node = self.conjunction(tokens)
		values = [node]
		while self.match(tokens.peek(), (TokenType.OR,)):
			op = tokens.pop()
			value = self.conjunction(tokens)
			values.append(value)
			node = BoolOp(op.value, values)
		return node
	@log
	def conjunction(self, tokens):
		node = self.inversion(tokens)
		values = [node]
		while self.match(tokens.peek(), (TokenType.AND,)):
			op = tokens.pop()
			value = self.conjunction(tokens)
			values.append(value)
			node = BoolOp(op.value, values)
		return node
	@log
	def inversion(self, tokens):
		if self.match(tokens.peek(), (TokenType.NOT,)):
			tokens.pop()
			inverse = self.inversion(tokens)
			node = Inverse(inverse)
		else:
			node = self.comparison(tokens)
		return node
	@log
	def comparison(self, tokens):
		node = self.sum(tokens)
		ops, comparators = [], [node]
		while self.match(tokens.peek(), (TokenType.LT, TokenType.GT, TokenType.LTE,
										TokenType.GTE, TokenType.EQ, TokenType.NE)):
			op = tokens.pop()
			comparator = self.sum(tokens)
			ops.append(op.value)
			comparators.append(comparator)
			node = Compare(ops, comparators)
		return node
	@log
	def sum(self, tokens):
		node = self.term(tokens)
		while self.match(tokens.peek(), (TokenType.PLUS, TokenType.MINUS)):
			op = tokens.pop()
			node = BinOp(node, op.value, self.term(tokens))
		return node
	@log
	def term(self, tokens):
		node = self.factor(tokens)
		while self.match(tokens.peek(), (TokenType.MULT, TokenType.DIV, TokenType.MOD)):
			op = tokens.pop()
			node = BinOp(node, op.value, self.factor(tokens))
		return node
	@log
	def factor(self, tokens):
		node = tokens.peek()
		if self.match(node, (TokenType.OPEN_PAREN,)):
			tokens.pop()
			node = self.expr(tokens)
			tokens.pop()
		elif self.match(node, (TokenType.IDENT,)):
			node = self.atom(tokens)
		else:
			node = self.atom(tokens)
		return node
	@log
	def atom(self, tokens):
		token = tokens.pop()
		self.callstack.push(token)
		if isfloat(token.value):
			node = Number(token.value)
		elif self.match(token, (TokenType.TRUE, TokenType.FALSE)):
			node = Boolean(token.value)
		elif self.match(token, (TokenType.EMPTY,)):
			node = Empty()
		elif self.match(token, (TokenType.CONST,)):
			node = String(token.value)
		elif self.match(token, (TokenType.IDENT,)):
			if self.match(token, (TokenType.STORE,)):
				node = Name(token.value, Context.STORE)
			else:
				node = Name(token.value, Context.LOAD)
		else:
			node = None
		return node

	def match(self, token, types):
		return getattr(token, 'type', None) in types