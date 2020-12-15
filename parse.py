from nodes import Number, BinOp, Expr, AST, Token


def log(fn):
	def util(*args, **kwargs):
		print(f'[{fn.__name__}]')
		return fn(*args, **kwargs)
	return util
		
		
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
			tree.add_node(self.expr(tokens))
		return tree
		
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
		if self.match(tokens.peek(), '('):
			tokens.dequeue()
			node = self.expr(tokens)
			tokens.dequeue()
		else:
			node = self.number(tokens)
		return node
	
	def number(self, tokens):
		return Number(tokens.dequeue().value)
		
	def match(self, token, char):
		return getattr(token, 'value', None) == char
	
