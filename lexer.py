# ply lexing

import ply.lex as lex

reserved = {
	'abs' : 'ABS',
}

tokens = ['INTCONST', 'IDENTIFIER', 'E'] + reserved.values()
literals = ('+', '-', '/', '*', '%', '(', ')')

# exponential
t_E = r'\*\*'

def t_IDENTIFIER(t) :
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	t.type = reserved.get(t.value, 'IDENTIFIER')
	return t

def t_INTCONST(t) :
	r'0|([1-9][0-9]*)'
	t.value = int(t.value)
	return t

def t_newline(t) :
	r'\n+'
	t.lexer.lineno += len(t.value)

t_ignore = ' \t'

# print token and skip ahead?
def t_error(t) :
	tok = t.value.split()[0]
	print 'Illegal token ' + tok
	t.lexer.skip(len(tok)) 	

lexer = lex.lex()
 
