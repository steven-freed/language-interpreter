# Interpreter #
Interpreter Written in Python. The Language is still in progress...

### EBNF Grammar ###
found in /src/grammar.md

### Quick Start: Repl ###
1. Clone Repo

2. Start Repl
```py
> python interpreter.py
```

3. Expressions
```py
> 2 + 4 * 5
22
```

Precedence (Default is Left Associative)
```py
> (2 + 4) % 5
1
> 2 + 4 % 5
6
> (FALSE AND TRUE) OR TRUE
TRUE
> FALSE AND (TRUE OR TRUE)
FALSE
```

4. Data Types; Empty, String, Number, Boolean
```py
> x ::= {}
> x ::= "hello"
> x ::= 'world'
> x ::= 123
> x ::= 123.45
> x ::= TRUE
> x ::= FALSE
```

* Functions and Lambda Functions
```py
> func foo(x, y) -> { 
    return x + y
}
> func bar(x, y) -> x * y
> foo(1, 2)
3
> bar(3, 3)
9
```

*To See History Press 'Up Arrow' Key*
