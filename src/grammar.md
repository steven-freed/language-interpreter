# Grammar
```
stmt:
    stmts
stmts:
    | singular_stmt
    | compound_stmt
singular_stmt:
    | expr
    | assign
    | return_stmt
return_stmt:
    'return' [expr]
compound_stmt:
    function_dec
function_dec:
    'func' [NAME] '(' [params] ')' '->' block
block:
    | '{' stmts '}'
    | singular_stmt
params:
    param [param_default] (',' | ')')
param_default:
    '=' expression
param:
    NAME
assign:
    NAME '::=' expr
expr:
    disjuncton
disjunction:
    conjunction { 'OR' conjunction }
conjunction:
    inversion { 'AND' inversion }
inversion:
    | 'NOT' inversion
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