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
compound_stmt:
    function_dec
function_dec:
    [NAME] '(' [params] ')' '->' block
block:
    | '{' statements '}'
    | singular_stmt
params:
    | parameters
parameters:
    | param_no_default
    | param_with_default
param_no_default:
    param (',' | ')')
param_with_default:
    param param_default (',' | ')')
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