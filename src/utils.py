def log(fn):
	def util(*args, **kwargs):
		print(f'[{fn.__name__}]')
		return fn(*args, **kwargs)
	return util

def isfloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


class Queue:

    def __init__(self, collection=[]):
	    self.q = collection
		
    def enqueue(self, node):
	    self.q.append(node)
        
    def dequeue(self):
        try:
            return self.q.pop(0)
        except IndexError:
            return None
    	
    def peek(self):
	    try:
		    return self.q[0]
	    except IndexError:
		    return None

    def clear(self):
	    self.q = []

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i < len(self.q):
            item = self.q[self.i]
            self.i += 1
            return item
        else:
            raise StopIteration

    def __reversed__(self):
        self.q.reverse()
        return self.q

    def __len__(self):
	    return len(self.q)
		
    def __str__(self):
	    return str([str(i) for i in self.q])


class Stack:

    def __init__(self, collection=[]):
	    self.stack = reversed(collection) if collection else []
    
    def push(self, node):
	    self.stack.append(node)
        
    def pop(self):
        try:
            return self.stack.pop()
        except IndexError:
            return None
    	
    def peek(self):
	    try:
		    return self.stack[len(self.stack) - 1]
	    except IndexError:
		    return None

    def clear(self):
	    self.stack = []

    def __iter__(self):
        self.i = len(self.stack)
        return self

    def __next__(self):
        if self.i >= 0:
            item = self.stack[self.i]
            self.i -= 1
            return item
        else:
            raise StopIteration

    def __len__(self):
	    return len(self.stack)
		
    def __str__(self):
	    return str([str(i) for i in self.stack])
