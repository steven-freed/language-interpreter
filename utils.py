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
        return self

    def __getitem__(self, key):
        return self.q[key]

    def __len__(self):
	    return len(self.q)
		
    def __str__(self):
	    return str([str(i) for i in self.q])