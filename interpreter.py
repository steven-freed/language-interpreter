import sys, traceback, readline
from abc import ABC, abstractmethod
from scanner import Scanner
from parser import Parser
from nodes import Context


class Visitor:

	@abstractmethod
	def visit_AST(self, ast):
		raise NotImplementedError(f'Please implement the visitor method for AST')

	@abstractmethod
	def visit_Expr(self, expr):
		raise NotImplementedError(f'Please implement the visitor method for Expr')
		
	@abstractmethod
	def visit_BinOp(self, binop):
		raise NotImplementedError(f'Please implement the visitor method for BinOp')
		
	@abstractmethod
	def visit_Number(self, number):
		raise NotImplementedError(f'Please implement the visitor method for Number')
	
		
class Interpreter(Visitor):
		
	def __init__(self):
		self.globalvars = {}

	def run(self, tree):
		self.interpret(tree)
		
	def interpret(self, tree):
		out = tree.accept(self)
		if all(out):
			print(*out)

	def visit_AST(self, ast):
		return [n.accept(self) for n in ast.get_nodes()]

	def visit_Stmt(self, stmt):
		return stmt.value.accept(self)

	def visit_Stmts(self, stmts):
		return stmts.value.accept(self)

	def visit_SingularStmt(self, singular_stmt):
		return singular_stmt.value.accept(self)

	def visit_Assign(self, assign):
		name = assign.target
		value = assign.value.accept(self)
		if name.context == Context.STORE:
			self.globalvars[name.ident] = value
		
	def visit_Expr(self, expr):
		return expr.value.accept(self)
		
	def visit_BinOp(self, binop):
		if binop.op == '+':
			return binop.left.accept(self) + binop.right.accept(self)
		elif binop.op == '-':
			return binop.left.accept(self) - binop.right.accept(self)
		elif binop.op == '*':
			return binop.left.accept(self) * binop.right.accept(self)
		elif binop.op == '/':
			return binop.left.accept(self) / binop.right.accept(self)
		elif binop.op == '%':
			return binop.left.accept(self) % binop.right.accept(self)
		 
	def visit_Name(self, name):
		if name.context == Context.LOAD:
			return self.globalvars[name.ident]
	
	def visit_Number(self, number):
		return number.value


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

	def __init__(self):
		self.scanner = Scanner()
		self.parser = Parser()
		self.interpreter = Interpreter()

	def run(self):
		print(self.HEADER.format(color=self.Color.HEADER, end=self.Color.END))
		while True:
			try:
				user_input = input(self.CMD.format(end=self.Color.END, color=self.Color.USER))
				if self.is_quit_cmd(user_input): break
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
	

if __name__ == '__main__':
	Repl().run()
