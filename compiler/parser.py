#!/usr/bin/python

import sys
import scanner, tree

class Parser:
	def __init__(self, sc):
		self._tokens = []
		while True:
			tok = sc.next_token()
			if tok == None:
				break
			else:
				self._tokens.append(tok)
		self._token_idx = 0
		self._tree = []
		self._stack = []
		self._tok_idx = 0
	
	def parse(self):
		self._push('PROG')
		self._parse_base_list()
		return self._pop('PROG')

	def _is_end_token(self):
		return (self._token_idx == len(self._tokens))

	def _parse_base_list(self):
		self._push('BASELIST')
		while (not self._is_end_token()) and (not self._next_token_is('}')):
			self._parse_base()
		self._pop('BASELIST')

	def _parse_base(self):
		self._push('BASE')
		if self._next_token_is('for'):
			self._parse_for()
		else:
			self._parse_statment()
			self._next(';')
		self._pop('BASE')

	def _parse_for(self):
		self._push('FOR')
		self._next('for')
		self._next('(')
		self._parse_statment()
		self._next(';')
		self._parse_cond()
		self._next(';')
		self._parse_statment()
		self._next(')')
		self._parse_block()
		self._pop('FOR')

	def _parse_block(self):
		self._push('BLOCK')
		self._next('{')
		self._parse_base_list()
		self._next('}')
		self._pop('BLOCK')

	def _parse_statment(self):
		self._push('STATMENT')
		if self._next_token_is('return'):
			self._next('return')
			self._next('id')
		else:
			self._next('id')
			if self._next_token_is('='):
				self._next('=')
				self._parse_exp()
			else:
				self._next('|++|--|')
		self._pop('STATMENT')

	def _parse_exp(self):
		self._push('EXP')
		self._next('|id|number|string|')
		if self._next_token_is('|+|-|*|/|'):
			self._next('|+|-|*|/|')
			self._next('|id|number|string|')
		self._pop('EXP')

	def _parse_cond(self):
		self._push('COND')
		self._parse_exp()
		self._next('|==|!=|<=|>=|<|>|')
		self._parse_exp()
		self._pop('COND')

	def _level(self):
		return len(self._stack)

	def _next_token_is(self, node_t):
		if self._token_idx == len(self._tokens):
			return False
		tok = self._tokens[self._token_idx]
		if tok.part_of_speech in node_t:
			return True
		else:
			return False

	def _next(self, node_t):
		tok = self._tokens[self._token_idx]
		if tok.part_of_speech in node_t:
			t = tree.Tree(tok.part_of_speech, tok.word)
			parent_t = self._stack[-1]
			parent_t.add_child(t)
			self._token_idx += 1
			return tok
		else:
			print('node_t mismatch')
			return None

	def _push(self, node_t):
		#print('>  '+(self._level()*'--')+':'+node_t)
		t = tree.Tree(node_t, '')
		self._stack.append(t)
		return t
	
	def _pop(self, node_t):
		t = self._stack.pop()
		#print('<  '+(self._level()*'--')+':'+t.ntype)
		if t.ntype != node_t:
			print("tree type mismatch")
			return None
		if self._stack:
			parent_t = self._stack[-1]
			parent_t.add_child(t)
		return t

if __name__ == "__main__":
	p = Parser(scanner.Scanner(sys.argv[1]))
	t = p.parse()
	t.print_tree(0)
