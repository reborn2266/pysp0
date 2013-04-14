#!/usr/bin/python

import sys

STRING_START 	= '\"'
STRING_END 		= '\"'
OPERATORS 		= '+-*/<=>!'
DIGITS 			= '0123456789'
ALPHAS 			= 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
KEYWORDS		= '|if|for|while|return|'
OPERATOR1 		= '|++|--|'
OPERATOR2 		= '|+|-|*|/|'
COND_OP			= '|==|!=|<=|>=|<|>|'
ITEM			= '|id|number|string|'
OP				= '+-*/<=>!'

STRING_T		= 'string'
NUMBER_T		= 'number'
ID_T			= 'id'

class Token:
	def __init__(self, word):
		self.word = word
		if word in KEYWORDS:
			self.part_of_speech = word
		elif word[0] == STRING_START:
			self.part_of_speech = STRING_T
		elif word[0] in DIGITS:
			self.part_of_speech = NUMBER_T
		elif word[0] in ALPHAS:
			self.part_of_speech = ID_T
		else:
			self.part_of_speech = word

class Scanner:
	def __init__(self, file_name):
		with open(file_name, 'r') as f:
			self._prog_src = f.read()
			self._cur_ch_idx = 0
			self._ch_len = len(self._prog_src)

	def _consume_until(self, start, group):
		while self._prog_src[self._cur_ch_idx] in group:
			self._cur_ch_idx += 1
			if self._cur_ch_idx >= self._ch_len:
				break
		tok = Token(self._prog_src[start:self._cur_ch_idx])
		#print(tok.word)
		#print(tok.part_of_speech)
		return tok

	def next_token(self):
		try:
			while True:
				ch = self._prog_src[self._cur_ch_idx]
				if ch == ' ' or ch == '\t' or ch == '\n':
					self._cur_ch_idx += 1
					continue
				else:
					break
			tok_begin = self._cur_ch_idx

			if ch == STRING_START:
				self._cur_ch_idx = self._prog_src.find(STRING_END, self._cur_ch_idx+1)
				if self._cur_ch_idx == -1:
					print("string mismatch")
					return None
				else:
					self._cur_ch_idx += 1
					tok = Token(self._prog_src[tok_begin:self._cur_ch_idx])
					#print(tok.word)
					#print(tok.part_of_speech)
					return tok
			elif ch in OPERATORS:
				return self._consume_until(tok_begin, OPERATORS)
			elif ch in DIGITS:
				return self._consume_until(tok_begin, DIGITS)
			elif ch in ALPHAS:
				return self._consume_until(tok_begin, ALPHAS+DIGITS)
			else:
				self._cur_ch_idx += 1
				tok = Token(self._prog_src[tok_begin:self._cur_ch_idx])
				#print(tok.word)
				#print(tok.part_of_speech)
				return tok
		
		except IndexError:
			return None
		return ch

if __name__ == "__main__":
	s = Scanner(sys.argv[1]);
	while s.next_token():
		pass
