from nodes import Visitor


class Symbol:

    def __init__(self, ident, scope, value, astnode):
        self.ident = ident
        self.scope = scope
        self.value = value
        self.astnode = astnode

    def __str__(self):
        return f'({self.ident},{self.scope},{self.value})'


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
        return "Symbol Table: " + ','.join([ident + str(sym) for ident, sym in self.table.items()])

    def run(self, tree):
        self.analyze(tree)
        print(str(self))
        return self

    def analyze(self, tree):
        tree.accept(self)
        
    def visit_AST(self, ast):
        [branch.accept(self) for branch in ast.branches]

    def visit_Expr(self, expr):
	    expr.value.accept(self)
        
    def visit_Assign(self, assign):
        name = assign.target
        value = assign.value.accept(self)
        node = assign.value
        self.add(
            Symbol(name.ident, Scope.BLOCK, value, node)
        )

    def visit_BinOp(self, binop):
        left, right = binop.left.accept(self), binop.right.accept(self)
       
    def visit_Compare(self, comp):
        [op.accept(self) for op in comp.ops], [comparator.accept(self) for comparator in comp.comparators]

    def visit_Name(self, name):
        return name

    def visit_Number(self, number):
        return number
    
    def visit_String(self, string):
        return string
    
    def visit_Empty(self, empty):
        return empty
