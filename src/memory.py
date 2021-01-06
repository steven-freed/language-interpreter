

class Memory:

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.memory = {}

    def add(self, ident, value):
        self.memory[ident] = value
        if self.verbose: print(f'[Memory] Stored {ident}')

    def get(self, ident):
        if self.verbose: print(f'[Memory] Loaded {ident}')
        return self.memory.get(ident)

    def discard(self, ident):
        del self.memory[ident]

    def __str__(self):
        return str(self.memory)
    

class Scope:
    GLOBAL = 'GLOBAL'
    BLOCK =  'BLOCK'


class Symbol:

    def __init__(self, ident, type_, scope, address=None):
        self.ident = ident
        self.type = type_
        self.scope = scope
        self.address = address

    def __str__(self):
        return f'({self.ident},{self.type},{self.address},{self.scope})'


class Heap(Memory):
    
    def __init__(self, verbose=False):
       super().__init__(verbose=verbose)


class SymbolTable(Memory):

   def __init__(self, verbose=False):
       super().__init__(verbose=verbose)
