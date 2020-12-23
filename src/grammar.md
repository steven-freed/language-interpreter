# Grammar
```
stmt:
    stmts
stmts:
    singular_stmt
singular_stmt:
    | expr
    | assign
assign:
    NAME '::=' expr
expr:
    term { ('+' | '-') term }
term:
    factor { ('*' | '/' | '%') factor }
factor:
    | '(' expr ')'
    | atom
atom:
    | NUMBER
    | NAME
    | STRING
    | boolean
    | empty
boolean:
    ('TRUE' | 'FALSE')
empty:
    '{}'
```