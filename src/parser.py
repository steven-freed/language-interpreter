from utils import (
	isfloat, isstr, isbool, isempty,
	log, Stack
)
from nodes import (
	Number, BinOp, Expr, AST, Token, Context, SingularStmt,
	Assign, Name, Stmt, Stmts, String, Boolean, Empty
)

		
class Parser:
	
	def run(self, tokens):
		self.callstack = Stack()
		tokenstack = Stack(collection=tokens)
		return self.parse(tokenstack)
	
	def parse(self, tokens):
		tree = AST()
		while len(tokens):
			tree.add_node(self.stmt(tokens))
		return tree
		
	def stmt(self, tokens):
		return Stmt(self.stmts(tokens))
	
	def stmts(self, tokens):
		return Stmts(self.singular_stmt(tokens))

	def singular_stmt(self, tokens):
		node = self.expr(tokens)
		if isinstance(node, Name) and self.match(tokens.peek(), '::='):
			tokens.push(self.callstack.pop())
			node = self.assign(tokens)
		return SingularStmt(node)

	def assign(self, tokens):
		name = self.atom(tokens)
		tokens.pop()
		value = self.expr(tokens)
		return Assign(name, value)

	def expr(self, tokens):
		node = self.term(tokens)
		while self.match(tokens.peek(), '+') or \
			self.match(tokens.peek(), '-'):
			op = tokens.pop()
			node = BinOp(node, op.value, self.term(tokens))
		return node

	def term(self, tokens):
		node = self.factor(tokens)
		while self.match(tokens.peek(), '*') or \
			self.match(tokens.peek(), '/') or \
			self.match(tokens.peek(), '%'):
			op = tokens.pop()
			node = BinOp(node, op.value, self.factor(tokens))
		return node

	def factor(self, tokens):
		node = tokens.peek()
		if self.match(node, '('):
			tokens.pop()
			node = self.expr(tokens)
			tokens.pop()
		elif node.type == 'id':
			node = self.atom(tokens)
		elif node.type == 'const':
			node = self.atom(tokens)
		return node

	def atom(self, tokens):
		token = tokens.pop()
		self.callstack.push(token)
		if isfloat(token.value):
			node = Number(token.value)
		elif isstr(token.value):
			node = String(token.value)
		elif isbool(token.value):
			node = Boolean(token.value)
		elif isempty(token.value):
			node = Empty()
		else:
			if self.match(tokens.peek(), '::='):
				node = Name(token.value, Context.STORE)
			else:
				node = Name(token.value, Context.LOAD)
		return node

	def match(self, token, char):
		return getattr(token, 'value', None) == char
	
