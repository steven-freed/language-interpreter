from nodes import (
    Visitor, BinOp
)
from exc import (
	TypeException, UndeclaredException
)

class SemanticAnalyzer(Visitor):

    def run(self, tree, symtable):
        self.symtable = symtable
        self.analyze(tree)

    def analyze(self, tree):
        tree.accept(self)
        
    def visit_AST(self, ast):
        [branch.accept(self) for branch in ast.branches]

    def visit_Expr(self, expr):
	    return expr.value.accept(self)
        
    def visit_Assign(self, assign):
        return assign.value.accept(self)

    def visit_BinOp(self, binop):
        print(binop.left, binop.right)
        left, op, right = binop.left.accept(self), binop.op, binop.right.accept(self)
        ltype, rtype = left.__class__.__name__, right.__class__.__name__
        if type(left) != type(right):
           raise TypeException(f'Cannot apply {op} operator to types {ltype} and {rtype}')
        else:
            # return node of same type for type compare
            return left or right
    
    def visit_Compare(self, comp):
        ops, comparators = [op for op in comp.ops], [comparator.accept(self) for comparator in comp.comparators]
        comptypes = [comp.__class__.__name__ for comp in comparators]
        if len(set(comptypes)) != 1:
            raise TypeException(f'Cannot apply {op} comparison to types {ltype} and {rtype}')

    def visit_Name(self, name):
        try:
            return self.symtable[name.ident].astnode
        except Exception:
            raise UndeclaredException(f'Attempted to use variable "{name.ident}" before declaration')

    def visit_Boolean(self, boolean):
        return boolean
        
    def visit_Number(self, number):
        return number
    
    def visit_String(self, string):
        return string
    
    def visit_Empty(self, empty):
        return empty
