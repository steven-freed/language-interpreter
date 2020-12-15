import sys
from pprint import pprint 
from scan import Scanner
from parse import Parser


class Visitor:
	
	def visit(self, node):
		visitor = getattr(self, 'visit_' + type(node).__name__)
		return visitor(node)
		
class Interpreter(Visitor):
		
	def run(self, tree):
		self.__interpret__(tree)
		
	def __interpret__(self, tree):
		return self.visit(tree)

	def visit_AST(self, node):
		return self.visit(node.module)
		
	def visit_Module(self, node):
		return [print(self.visit(n), flush=True) for n in node.body]
		
	def visit_Expr(self, node):
		return self.visit(node.value)
		
	def visit_BinOp(self, node):
		if node.op == '+':
			return self.visit(node.left) + self.visit(node.right)
		elif node.op == '-':
			return self.visit(node.left) - self.visit(node.right)
		elif node.op == '*':
			return self.visit(node.left) * self.visit(node.right)
		elif node.op == '/':
			return self.visit(node.left) / self.visit(node.right)
		elif node.op == '%':
			return self.visit(node.left) % self.visit(node.right)
		 
	def visit_Number(self, node):
		return node.value


scanner = Scanner()
parser = Parser()
interpreter = Interpreter()
while True:
	print('> ', end='')
	user_input = input()
	if user_input.lower() in ('quit','q'):
		break
	tokens = scanner.run(user_input)
	tree = parser.run(tokens)
	interpreter.run(tree)
print('Good Bye')
