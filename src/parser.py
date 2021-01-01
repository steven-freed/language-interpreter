from utils import (
	isfloat, isbool, isempty,
	log, Stack
)
from nodes import (
	Number, BinOp, Expr, AST, Token, Context,
	Assign, Name, String, Boolean, Empty, Compare,
	BoolOp, Inverse
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
		return tree
		
	def stmt(self, tokens):
		return self.stmts(tokens)
	
	def stmts(self, tokens):
		return self.singular_stmt(tokens)

	def singular_stmt(self, tokens):
		node = self.expr(tokens)
		if isinstance(node.value, Name) and self.match(tokens.peek(), '::='):
			tokens.push(self.callstack.pop())
			node = self.assign(tokens)
		return node

	def assign(self, tokens):
		name = self.atom(tokens)
		tokens.pop()
		value = self.expr(tokens)
		return Assign(name, value)
	
	def expr(self, tokens):
		return Expr(self.disjunction(tokens))
	
	def disjunction(self, tokens):
		node = self.conjunction(tokens)
		values = [node]
		while self.match(tokens.peek(), 'OR'):
			op = tokens.pop()
			value = self.conjunction(tokens)
			values.append(value)
			node = BoolOp(op.value, values)
		return node
	
	def conjunction(self, tokens):
		node = self.inversion(tokens)
		values = [node]
		while self.match(tokens.peek(), 'AND'):
			op = tokens.pop()
			value = self.conjunction(tokens)
			values.append(value)
			node = BoolOp(op.value, values)
		return node
	
	def inversion(self, tokens):
		if self.match(tokens.peek(), 'NOT'):
			tokens.pop()
			inverse = self.inversion(tokens)
			node = Inverse(inverse)
		else:
			node = self.comparison(tokens)
		return node
	
	def comparison(self, tokens):
		node = self.sum(tokens)
		ops, comparators = [], [node]
		while self.match(tokens.peek(), '=') or \
			self.match(tokens.peek(), '<>') or \
			self.match(tokens.peek(), '<=') or \
			self.match(tokens.peek(), '<') or \
			self.match(tokens.peek(), '>=') or \
			self.match(tokens.peek(), '>'):
			op = tokens.pop()
			comparator = self.sum(tokens)
			ops.append(op.value)
			comparators.append(comparator)
			node = Compare(ops, comparators)
		return node
	
	def sum(self, tokens):
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
		elif isbool(token.value):
			node = Boolean(token.value)
		elif isempty(token.value):
			node = Empty()
		elif token.type == 'const':
			node = String(token.value)
		elif token.type == 'id':
			if self.match(tokens.peek(), '::='):
				node = Name(token.value, Context.STORE)
			else:
				node = Name(token.value, Context.LOAD)
		return node

	def match(self, token, char):
		return getattr(token, 'value', None) == char
	
