# Simple Math Grammar Interpreter #
Interpreter written in Python, C version in the works with a full language implementation.

### EBNF Grammar ###
```
expr:       term { ('+' | '-') term }
term:       factor { ('*' | '/' | '%') factor }
factor:     '(' expr ')' | number
```

### Quick Start: Repl ###
1. Clone Repo

2. Start Repl
```py
> python interpreter.py
```

3. Enter Expression
```py
> 2 + 4 * 5
22
```

If Needed, Use Precedence
```py
> (2 + 4) % 5
1
> 2 + 4 % 5
6
```

4. Add Variables
```py
> x ::= 5
> x + 5
10
```

See History Press 'Up Arrow' Key
