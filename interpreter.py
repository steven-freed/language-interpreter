import sys, traceback
from scan import Scanner
from parse import Parser


class Visitor:
	
	def visit(self, node):
		visitor = getattr(self, 'visit_' + type(node).__name__)
		return visitor(node)
		
class Interpreter(Visitor):
		
	def run(self, tree):
		self.interpret(tree)
		
	def interpret(self, tree):
		return self.visit(tree)

	def visit_AST(self, node):
		return [print(self.visit(n)) for n in node.get_nodes()]
		
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

class Repl:

	class Color:
		HEADER = '\033[93m'
		USER = '\033[92m'
		END = '\033[0m'
	HEADER = (
		'{color}Math Grammar Interpreter v1.0\n'
		'Type "quit", "q", or "ctr-c" to exit interpreter.{end}'
	)
	EXIT = 	'{color}Good Bye{end}'
	CMD = 	'{end}> {color}'
	EXC = 	'{exc}{end}'
	QUIT_CMDS = (
		'quit', 'q'
	)
	HIST_CMDS = (
		'last'
	)

	def __init__(self):
		self.history_stack = []
		self.scanner = Scanner()
		self.parser = Parser()
		self.interpreter = Interpreter()

	def run(self):
		print(self.HEADER.format(color=self.Color.HEADER, end=self.Color.END))
		while True:
			try:
				user_input = input(self.CMD.format(end=self.Color.END, color=self.Color.USER))
				if self.is_quit_cmd(user_input): break
				if self.is_hist_cmd(user_input): continue
				self.add_to_history(user_input)
				tokens = self.scanner.run(user_input)
				tree = self.parser.run(tokens)
				self.interpreter.run(tree)
			except KeyboardInterrupt:
				print('\n' + self.EXIT.format(color=self.Color.HEADER, end=self.Color.END))
				break
			except Exception:
				print(self.EXC.format(exc=traceback.format_exc(), end=self.Color.END))
				continue

	def is_quit_cmd(self, user_input):
		if user_input.lower() in self.QUIT_CMDS:
			print(self.EXIT.format(color=self.Color.HEADER, end=self.Color.END))
			return True
		else:
			return False

	def is_hist_cmd(self, user_input):
		if user_input.lower() in self.HIST_CMDS:
			try:
				print(self.history_stack.pop())
			except IndexError:
				print('No more history available')
			return True
		else:
			return False

	def add_to_history(self, user_input):
		self.history_stack.append(user_input)
	

if __name__ == '__main__':
	Repl().run()
