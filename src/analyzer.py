from nodes import (
    Visitor, BinOp, Context, Return
)
from memory import (
    SymbolTable, Symbol, Scope
)
from exc import (
	UndeclaredException, ArgException
)


class SemanticAnalyzer(Visitor):

    def __init__(self):
        self.symtable = SymbolTable()

    def run(self, tree):
        self.analyze(tree)

    def analyze(self, tree):
        tree.accept(self)
        
    def visit_AST(self, ast):
        [branch.accept(self) for branch in ast.branches]

    def visit_Expr(self, expr):
	    expr.value.accept(self)
        
    def visit_Assign(self, assign):
        name = assign.target
        self.symtable.add(name.ident, Symbol(name.ident, type(assign.value), Scope.GLOBAL))
        value = assign.value.accept(self)

    def visit_BinOp(self, binop):
        binop.left.accept(self)
        binop.right.accept(self)

    def visit_BoolOp(self, boolop):
        [value.accept(self) for value in boolop.values]
    
    def visit_Compare(self, comp):
        [comparator.accept(self) for comparator in comp.comparators]

    def visit_Name(self, name):
        if not self.symtable.get(name.ident):
            raise UndeclaredException(f'Attempted to use variable "{name.ident}" before declaration')

    def visit_Function(self, fn):
        #self.symtable.add(fn.ident, Symbol(fn.ident, type(fn), Scope.GLOBAL))
        defaults_started = False
        for arg in fn.args:
            if arg.default:
                defaults_started = True
            if not arg.default and defaults_started:
                raise ArgException(f'Non-default valued argument "{arg.ident}" follows default valued argument')
            self.symtable.add(arg.ident, Symbol(arg.ident, type(arg.default), fn.ident))

    def visit_FunctionCall(self, call):
        if not self.symtable.get(call.ident):
            raise UndeclaredException(f'Attempted to call function "{call.ident}" before declaration')

    def visit_Return(self, returns):
        if returns.value:
            returns.value.accept(self)

    def visit_Arg(self, arg):
        pass

    def visit_Inverse(self, inverse):
        inverse.value.accept(self)
    
    def visit_Boolean(self, boolean):
        return boolean
        
    def visit_Number(self, number):
        return number
    
    def visit_String(self, string):
        return string
    
    def visit_Empty(self, empty):
        return empty
