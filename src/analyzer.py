from nodes import (
    Visitor, BinOp, Context
)
from memory import (
    SymbolTable, Symbol, Scope
)
from exc import (
	UndeclaredException
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
        assign.value.accept(self)

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

    def visit_Boolean(self, boolean):
        return boolean
        
    def visit_Number(self, number):
        return number
    
    def visit_String(self, string):
        return string
    
    def visit_Empty(self, empty):
        return empty
