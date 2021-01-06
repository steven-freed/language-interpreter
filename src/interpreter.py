import sys, traceback, readline, math
from scanner import Scanner
from parser import Parser
from nodes import (
	Context, Boolean, BinOp, Compare, BoolOp, Return
)
from analyzer import SemanticAnalyzer
from memory import Heap, Symbol, Scope
from nodes import Visitor
from exc import (
	TypeException
)
	

class Interpreter(Visitor):

	def __init__(self, verbose=False):
		self.heap = Heap(verbose=verbose)

	def run(self, tree):
		self.interpret(tree)
		
	def interpret(self, tree):
		out = tree.accept(self)
		if None not in out and out:
			print(*out, file=sys.stdout)

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
			self.heap.add(name.ident, Symbol(name.ident, type(value), Scope.BLOCK, address=value))
		
	def visit_Expr(self, expr):
		return expr.value.accept(self)
		
	def visit_BinOp(self, binop):
		left, right = binop.left.accept(self), binop.right.accept(self)
		if type(left) != type(right):
			raise TypeException(f'Cannot apply {binop.op} operator to types {left.__class__.__name__} and {right.__class__.__name__}')
		else:
			result_node = type(left) or type(right)
			result_value = BinOp.OP_MAP[binop.op](left.value, right.value)
			return result_node(result_value)

	def visit_BoolOp(self, boolop):
		op, values = boolop.op, [value.accept(self) for value in boolop.values]
		for i in range(len(values) - 1):
			a, b = values[i], values[i + 1]
			result_value = BoolOp.OP_MAP[op](a.value, b.value)
			result_node = type(a) if result_value == a.value else type(b)
		return result_node(result_value)

	def visit_Compare(self, comp):
		ops, comparators = [op for op in comp.ops], [comparator.accept(self) for comparator in comp.comparators]
		result = True
		for i, op in enumerate(ops):
			a, b = comparators[i].value, comparators[i + 1].value
			result = result and Compare.OP_MAP[op](a, b)
		return Boolean(result)

	def visit_FunctionDec(self, fn):
		self.heap.add(fn.ident, Symbol(fn.ident, type(fn), Scope.GLOBAL, address=fn))
		for arg in fn.args:
			arg.accept(self)
			self.heap.add(arg.ident, Symbol(arg.ident, type(arg.default), fn.ident, address=arg))

	def visit_FunctionCall(self, call):
		fn = self.heap.get(call.ident).address
		for call_val, arg in zip(call.args, fn.args):
			# replaces Arg nodes with function call param values by binding
			# call values to function Arg node idents
			arg = self.heap.get(arg.ident)
			self.heap.add(arg.ident, Symbol(arg.ident, type(call_val.value), fn.ident, address=call_val))
		returns = None
		for node in fn.body:
			value = node.accept(self)
			if isinstance(node, Return) or fn.lambda_:
				returns = value
		return returns

	def visit_Return(self, returns):
		return returns.value.accept(self) if returns.value else None
			
	def visit_Arg(self, arg):
		return arg.default.accept(self) if arg.default else None
		 
	def visit_Name(self, name):
		if name.context == Context.LOAD:
			return self.heap.get(name.ident).address

	def visit_Inverse(self, inverse):
		node = inverse.value
		inverse_value = not node.value
		node = type(node)
		return node(inverse_value)

	def visit_Number(self, number):
		return number
	
	def visit_String(self, string):
		return string

	def visit_Boolean(self, boolean):
		return boolean

	def visit_Empty(self, empty):
		return empty



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
		self.analyzer = SemanticAnalyzer()
		self.interpreter = Interpreter(verbose=True)

	def run(self):
		print(self.HEADER.format(color=self.Color.HEADER, end=self.Color.END))
		while True:
			try:
				user_input = input(self.CMD.format(end=self.Color.END, color=self.Color.USER))
				if self.is_quit_cmd(user_input): break
				tokens = self.scanner.run(user_input)
				tree = self.parser.run(tokens)
				self.analyzer.run(tree)
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
