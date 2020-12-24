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
    disjuncton
disjunction:
    conjunction { 'OR' conjunction }
conjunction:
    inversion { 'AND' inversion }
inversion:
    | '~' inversion
    | comparison
comparison:
    sum { ('=' | '<>' | '<=' | '<' | '>=' | '>') sum }
sum:
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