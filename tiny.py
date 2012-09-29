#!/usr/bin/python
import sys


from parser import parser

def main() :

	print 'Enter a tiny expression.'


	try :
		s = raw_input('-> ').strip()
	except EOFError :
		sys.exit()	

	if s :
		exp = parser.parse(s)
		
		try :
			print 'Evaluating ' + exp.to_s()
			print exp.eval()
		except ZeroDivisionError, e :
			print e


if __name__ == '__main__' :
	main()
