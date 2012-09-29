import ply.yacc as yacc
from lexer import tokens
from tree import *

precedence = (
	('left', '+', '-'),
	('left', '*', '/', '%'),
	('right', 'u-'),
	('right', 'E'),
)

def p_error(p) :
	print 'Syntax error on token ' + p.value 

def p_binop(p) :
	'''
	exp : exp '+' exp
	    | exp '-' exp
        | exp '*' exp
	    | exp '/' exp
		| exp '%' exp
		| exp E exp
	'''
	p[0] = BinaryOp(p.lineno(1), p[2], p[1], p[3]) 

def p_ident(p) :
	'''
	exp : IDENTIFIER
	'''
	p[0] = Identifier(p.lineno(1), p[1])

def p_intconst(p) :
	'''	
	exp : INTCONST
	'''
	p[0] = Intconst(p.lineno(1), p[1])

def p_group(p) :
	'''
	exp : '(' exp ')'
	'''
	p[0] = p[2]	

def p_abs(p) :	
	'''
	exp : ABS '(' exp ')' 
	'''
	p[0] = AbsOp(p.lineno(1), p[3])
	
def p_unary_minus(p) :
	'''
	exp : '-' exp %prec u-
	'''
	p[0] = BinaryOp(p.lineno(1), '-', Intconst(p.lineno(1), 0), p[2])

parser = yacc.yacc()
