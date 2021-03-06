from utils import (
	isfloat, log, Stack
)
from tokens import Token, TokenType
from nodes import (
	Number, BinOp, Expr, AST, Context,
	Assign, Name, String, Boolean, Empty, Compare,
	BoolOp, Inverse, Function, Arg, Return,
	FunctionCall
)

		
class Parser:
	
	def run(self, tokens):
		self.callstack = Stack()
		tokenstack = Stack(collection=tokens)
		return self.parse(tokenstack)
	
	def parse(self, tokens):
		tree = AST()
		while len(tokens):
			stmt = self.stmt(tokens)
			tree.add_branch(stmt)
		print('AST\t', tree.branches)
		return tree
	@log
	def stmt(self, tokens):
		return self.stmts(tokens)
	@log
	def stmts(self, tokens):
		node = self.singular_stmt(tokens)
		return node
	@log
	def function_dec(self, tokens):
		def get_args(tokens):
			args = []
			while not self.match(tokens.peek(), (TokenType.CLOSED_PAREN,)):
				token = tokens.peek()
				if self.match(token, (TokenType.IDENT,)):
					arg = self.params(tokens)
					args.append(arg)
				else:
					tokens.pop()
			return args
		node = None
		if self.match(tokens.peek(), (TokenType.OPEN_PAREN,)):
			tokens.pop()
			args = get_args(tokens)
			if self.match(tokens.peek(), (TokenType.CLOSED_PAREN,)):
				tokens.pop() # pop closing paren
				body = []
				if self.match(tokens.peek(), (TokenType.OPEN_BRACE,)):
					fnbody = self.block(tokens)
				if fnbody:
					body.append(fnbody)
				if self.match(tokens.peek(), (TokenType.CLOSED_BRACE,)):
					tokens.pop()
					node = Function(args, body=body)
		if not node:
			raise SyntaxError(f'Invalid function declaration')
		return node
	@log
	def block(self, tokens):
		return self.stmts(tokens)
	@log
	def params(self, tokens):
		param = self.param(tokens)
		param_def = None
		if self.match(tokens.peek(), (TokenType.EQ,)):
			param_def = self.param_default(tokens)
		return Arg(param, default=param_def)
	@log
	def param_default(self, tokens):
		default = None
		if self.match(tokens.peek(), (TokenType.EQ,)):
			tokens.pop()
			default = self.atom(tokens)
		return default
	@log
	def param(self, tokens):
		name = self.atom(tokens)
		return getattr(name, 'ident', None)
	@log
	def singular_stmt(self, tokens):
		if self.match(tokens.peek(), (TokenType.RETURN,)):
			tokens.pop()
			node = Return(self.expr(tokens))
		elif self.match(tokens.peek(), (TokenType.IDENT,)):
			node = self.assign(tokens)
		else:
			node = self.expr(tokens)
		if not node:
			tokens.push(self.callstack.pop())
			node = self.expr(tokens)
		return node
	@log
	def assign(self, tokens):
		node = None
		name = self.atom(tokens)
		if self.match(tokens.peek(), (TokenType.STORE,)):
			tokens.pop()
			if self.match(tokens.peek(), (TokenType.FUNC,)):
				tokens.pop()
				value = self.function_dec(tokens)
			else:
				value = self.expr(tokens)
			node = Assign(name, value)
		return node
	@log
	def expr(self, tokens):
		node = self.disjunction(tokens)
		if node:
			node = Expr(node)
		return node
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
		else:
			node = self.invocation(tokens)
		return node
	@log
	def invocation(self, tokens):
		node = self.atom(tokens)
		if isinstance(node, Name) and self.match(tokens.peek(), (TokenType.OPEN_PAREN,)):
			open_paren = tokens.pop()
			params = self.args(tokens)
			node = FunctionCall(node.ident, params)
			closed_paren = tokens.pop()
		return node
	@log
	def args(self, tokens):
		comma, args = tokens.peek(), []
		while not self.match(comma, (TokenType.CLOSED_PAREN,)):
			arg = self.arg(tokens)
			args.append(arg)
			comma = tokens.pop()
		return args
	@log
	def arg(self, tokens):
		atom = self.atom(tokens)
		return atom
	@log
	def atom(self, tokens):
		token = tokens.pop()
		node = None
		if isfloat(token.value):
			node = Number(token.value)
		elif self.match(token, (TokenType.TRUE, TokenType.FALSE)):
			node = Boolean(token.value)
		elif self.match(token, (TokenType.EMPTY,)):
			node = Empty()
		elif self.match(token, (TokenType.CONST,)):
			node = String(token.value)
		elif self.match(token, (TokenType.IDENT,)):
			if self.match(tokens.peek(), (TokenType.STORE, TokenType.OPEN_PAREN)):
				node = Name(token.value, Context.STORE)
			elif not self.match(tokens.peek(), (TokenType.OPEN_PAREN,)): # not a function dec
				node = Name(token.value, Context.LOAD)
		if node: self.callstack.push(token)
		return node

	def match(self, token, types):
		return getattr(token, 'type', None) in types