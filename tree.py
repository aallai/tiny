# AST for the tiny language, python version

from operator import *

# base class for all expressions
class Exp(object) :
	
	# leaf nodes like intconsts or ids have no prec
	def __init__(self, line, prec=None, parent=None) :
		self.line = line
		self.prec = prec
		self.parent = parent

	def eval(self) : pass

	def to_s(self, op=gt) :
		if self.prec is not None and self.parent and op(self.parent.prec, self.prec) :
			return '(%s)'
		else :
			return '%s'

class AbsOp(Exp) :

	def __init__(self, line, exp) :
		Exp.__init__(self, line, 0)
		self.exp = exp
		exp.parent = self

	def eval(self) :
		exp = self.exp.eval()
		
		if type(exp) is str :
			return ' '.join(['abs', '(', exp, ')']) 
		else :
			return abs(self.exp.eval())

	def to_s(self) :
		return 'abs(' + self.exp.to_s() + ')'

class BinaryOp(Exp) :

	def op_gen(op, string_op) :
		def func(x, y) :
			if str in (type(x), type(y)) :
				return string_op(str(x), str(y))
			else :
				return op(x, y)
		return func

	def string_op_gen(op) :
		def func(x, y) :
			return ' '.join([x, op, y])
		return func	

	# multiplication is a special case
	def string_mul(x, y) :
		if '0' in (x, y) :
			return '0'
		else :
			return ' '.join([x, '*', y])

	ops = {
		'+' : op_gen(add, string_op_gen('+')),
		'-' : op_gen(sub, string_op_gen('-')),
		'*' : op_gen(mul, string_mul),
		'/' : op_gen(div, string_op_gen('/')),
		'%' : op_gen(mod, string_op_gen('%')),
		'**' : op_gen(pow, string_op_gen('**')),			
	}

	op_precs = {
		'+' : 0,
		'-' : 0,
		'*' : 1,
        '/' : 1,
		'%' : 1,
        '**' : 3,
	}
		
	# left and right are Exps, op is a function
	def __init__(self, line, op, left, right) :
		Exp.__init__(self, line, BinaryOp.op_precs[op])
		self.op = BinaryOp.ops[op]
		self.left = left
		left.parent = self
		self.right = right
   		right.parent = self

	def eval(self) :
		return self.op(self.left.eval(), self.right.eval())

	def get_op(self) :
		return [k for k, v in BinaryOp.ops.items() if v == self.op][0]

	def to_s(self) :
		# special cases ugh
		op = gt
		if self.parent is not None and isinstance(self.parent, BinaryOp) and self.parent.get_op() in ('-', '/', '%') :
			op = ge
		return Exp.to_s(self, op) % ' '.join([self.left.to_s(), self.get_op(), self.right.to_s()])

class Identifier(Exp) :
	
	def __init__(self, line, ident) :
		Exp.__init__(self, line)
		self.ident = ident

	def eval(self) :
		return self.ident

	def to_s(self) :
		return self.ident

class Intconst(Exp) :

	def __init__(self, line, val) :
		Exp.__init__(self, line)
		self.val = val

	def eval(self) :
		return self.val

	def to_s(self) :
		return str(self.val)
