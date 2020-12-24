import sys, traceback, readline, operator
from utils import apply_operator
from scanner import Scanner
from parser import Parser
from nodes import Context
from analyzer import SemanticAnalyzer
from nodes import Visitor
from symbols import SymbolTable, Symbol, Scope
	
		
class Interpreter(Visitor):

	def run(self, tree, symtable):
		self.symtable = symtable
		self.interpret(tree)
		
	def interpret(self, tree):
		out = tree.accept(self)
		if None not in out:
			print(*out)

	def visit_AST(self, ast):
		return [branch.accept(self) for branch in ast.branches]

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
			self.symtable.add(Symbol(name.ident, Scope.BLOCK, value, assign.value))
		
	def visit_Expr(self, expr):
		return expr.value.accept(self)
		
	def visit_BinOp(self, binop):
		left, right = binop.left.accept(self), binop.right.accept(self)
		opmap = {
			'+': operator.add, '-': operator.sub,
			'*': operator.mul, '/': operator.truediv,
			'%': operator.mod
		}
		return opmap[binop.op](left, right)

	def visit_Compare(self, comp):
		opmap = {
			'=': operator.eq, '<>': operator.ne,
			'<': operator.lt, '>': operator.gt,
			'<=': operator.le, '>=': operator.ge,
			'OR': lambda a,b: a or b, 'AND': lambda a,b: a and b
		}
		ops, comparators = [op for op in comp.ops], [comparator.accept(self) for comparator in comp.comparators]
		result = True
		for i, op in enumerate(ops):
			a, b = comparators[i], comparators[i + 1]
			result = result and opmap[op](a, b)
		return result
		 
	def visit_Name(self, name):
		if name.context == Context.LOAD:
			return self.symtable[name.ident].value
	
	def visit_Number(self, number):
		return number.value
	
	def visit_String(self, string):
		return string.value

	def visit_Boolean(self, boolean):
		return boolean.value

	def visit_Empty(self, empty):
		return empty.value



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
		self.symtable = SymbolTable()
		self.scanner = Scanner()
		self.parser = Parser()
		self.analyzer = SemanticAnalyzer()
		self.interpreter = Interpreter()

	def run(self):
		print(self.HEADER.format(color=self.Color.HEADER, end=self.Color.END))
		while True:
			try:
				user_input = input(self.CMD.format(end=self.Color.END, color=self.Color.USER))
				if self.is_quit_cmd(user_input): break
				tokens = self.scanner.run(user_input)
				tree = self.parser.run(tokens)
				#symtable = self.symtable.run(tree)
				#self.analyzer.run(tree, self.symtable)
				self.interpreter.run(tree, self.symtable)
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
