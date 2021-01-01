# Interpreter #
Interpreter Written in Python. The language currently supports Mathmatical operations & comparisons, boolean operations, and variables.

### EBNF Grammar ###
found in /src/grammar.md

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

If Needed Use Precedence (Default is Left Associative)
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

4. Declare variables for types; Empty, String, Number, Boolean
```py
> x ::= {}
> x ::= "hello"
> x ::= 'world'
> x ::= 123
> x ::= 123.45
> x ::= TRUE
> x ::= FALSE
```

*To See History Press 'Up Arrow' Key*
