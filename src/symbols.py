from nodes import Visitor


class Symbol:

    def __init__(self, ident, scope, astnode):
        self.ident = ident
        self.scope = scope
        self.astnode = astnode

    def __str__(self):
        return f'{self.ident} {self.scope} {self.astnode}'


class Scope:
    GLOBAL = 1
    BLOCK = 2


class SymbolTable(Visitor):

    def __init__(self):
        self.table = {}

    def add(self, symbol):
        self.table[symbol.ident] = symbol

    def remove(self, name):
        del self.table[symbol.ident]

    def __getitem__(self, key):
        return self.table[key]

    def __str__(self):
        return "Symbol Table: " + ','.join([ident for ident, _ in self.table.items()])

    def run(self, tree):
        self.analyze(tree)
        return self

    def analyze(self, tree):
        tree.accept(self)
        
    def visit_AST(self, ast):
        [branch.accept(self) for branch in ast.branches]

    def visit_Expr(self, expr):
	    expr.value.accept(self)
        
    def visit_Assign(self, assign):
        name = assign.target
        value = assign.value
        self.add(
            Symbol(name.ident, Scope.BLOCK, value)
        )

    def visit_BinOp(self, binop):
        binop.left.accept(self), binop.right.accept(self)
       
    def visit_Name(self, name):
        pass

    def visit_Number(self, number):
        pass
    
    def visit_String(self, string):
        pass
    
    def visit_Empty(self, empty):
        pass
