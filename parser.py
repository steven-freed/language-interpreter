from utils import isfloat, log
from nodes import (
	Number, BinOp, Expr, AST, Token, Context, SingularStmt,
	Assign, Name, Stmt, Stmts
)

		
class Parser:
	'''
	Grammar
		expr: term { ('+' | '-') term }
		term: factor { ('*' | '/' | '%') factor }
		factor: number
	'''
	def run(self, tokens):
		return self.parse(tokens)
	
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
			tokens.dequeue()
			value = self.expr(tokens)
			node = Assign(node, value)
		return SingularStmt(node)

	def expr(self, tokens):
		node = self.term(tokens)
		while self.match(tokens.peek(), '+') or \
			self.match(tokens.peek(), '-'):
			op = tokens.dequeue()
			node = BinOp(node, op.value, self.term(tokens))
		return node

	def term(self, tokens):
		node = self.factor(tokens)
		while self.match(tokens.peek(), '*') or \
			self.match(tokens.peek(), '/') or \
			self.match(tokens.peek(), '%'):
			op = tokens.dequeue()
			node = BinOp(node, op.value, self.factor(tokens))
		return node

	def factor(self, tokens):
		node = tokens.peek()
		if self.match(node, '('):
			tokens.dequeue()
			node = self.expr(tokens)
			tokens.dequeue()
		elif node.type == 'id':
			node = self.atom(tokens)
		elif node.type == 'const':
			node = self.atom(tokens)
		return node

	def atom(self, tokens):
		token = tokens.dequeue()
		if isfloat(token.value):
			node = Number(token.value)
		else:
			if self.match(tokens.peek(), '::='):
				node = Name(token.value, Context.STORE)
			else:
				node = Name(token.value, Context.LOAD)
		return node

	def match(self, token, char):
		return getattr(token, 'value', None) == char
	
