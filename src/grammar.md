# Grammar
```
stmt:
    stmts
stmts:
    | singular_stmt
singular_stmt:
    | expr
    | assign
    | return_stmt
return_stmt:
    'return' [expr]
function_dec:
    'func' '(' [params] ')' block
block:
    '{' stmts '}'
params:
    | param [param_default] [‘,’]
param_default:
    '=' expression
param:
    NAME
assign:
    NAME '::=' ( expr | function_dec )
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
    | invocation
invocation:
    | NAME '(' [args] ')'
    | atom
args:
    | arg [',']
arg:
    | atom [‘,’]
    | function_dec [‘,’]
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