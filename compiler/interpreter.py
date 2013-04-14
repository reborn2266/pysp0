#!/usr/bin/python

import sys
import scanner, parser

variables = {}

def interpret(ast):
	if ast.ntype == 'PROG':
		interpret(ast.childs[0])
	elif ast.ntype == 'BASELIST':
		for base in ast.childs:
			interpret(base)
	elif ast.ntype == 'BASE':
		for base in ast.childs:
			interpret(base)
	elif ast.ntype == 'STATMENT':
		if ast.childs[0].ntype == 'id':
			variables[ast.childs[0].val] = interpret(ast.childs[2])
		elif ast.childs[0].ntype == 'return':
			if ast.childs[1].ntype == 'id':
				print(variables[ast.childs[1].val])
	elif ast.ntype == 'EXP':
		if ast.childs[0].ntype == 'number':
			return int(ast.childs[0].val)
		

if __name__ == '__main__':
	p = parser.Parser(scanner.Scanner(sys.argv[1]))
	interpret(p.parse())
