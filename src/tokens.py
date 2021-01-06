from enum import Enum


class TokenType(Enum):
    ARROW =         0
    CONST =         1
    IDENT =         2
    GT =            3
    LT =            4
    GTE =           5
    LTE =           6
    EQ =            7
    NE =            8
    MINUS =         9
    PLUS =          10
    MULT =          11
    DIV =           12
    MOD =           13
    TRUE =          14
    FALSE =         15
    AND =           16
    OR =            17
    NOT =           18
    EMPTY =         19
    RETURN =        20
    OPEN_PAREN =    21
    CLOSED_PAREN =  22
    OPEN_BRACE =    23
    CLOSED_BRACE =  24
    STORE =         25
    COMMA =         26
    FUNC =          27


class Token:
	
	def __init__(self, type, value, lineinfo):
		self.type = type
		self.value = value
		self.lineinfo = lineinfo # tuple (lineno, lineoff)
		
	def __str__(self):
		data = self.type, self.value, self.lineinfo
		return str(data)