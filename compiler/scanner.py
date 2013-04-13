#!/usr/bin/python

import sys, re

class Token:
	STRING 		= 'string'
	OPERATOR 	= 'operator'
	DIGIT 		= 'digit'
	ALPHA 		= 'alpha'

	def __init__(self, part_of_speech, word):
		self.part_of_speech = part_of_speech
		self.word = word

class Scanner:
	STRING_START 	= '\"'
	STRING_END 		= '\"'
	OPERATORS 		= '+-*/<=>!'
	DIGITS 			= '0123456789'
	ALPHAS 			= 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

	def __init__(self, file_name):
		with open(file_name, 'r') as f:
			self._prog_src = re.sub(r'\s', '', f.read())
			self._cur_ch_idx = 0
			self._ch_len = len(self._prog_src)

	def _consume_until(self, start, group, tok_type):
		while self._prog_src[self._cur_ch_idx] in group:
			self._cur_ch_idx += 1
			if self._cur_ch_idx >= self._ch_len:
				break
		tok = Token(tok_type, self._prog_src[start:self._cur_ch_idx])
		print(tok.word)
		print(tok.part_of_speech)
		return tok

	def next_token(self):
		try:
			ch = self._prog_src[self._cur_ch_idx]
			tok_begin = self._cur_ch_idx

			if ch == Scanner.STRING_START:
				self._cur_ch_idx = self._prog_src.find(Scanner.STRING_END, self._cur_ch_idx+1)
				if self._cur_ch_idx == -1:
					print("string mismatch")
					return None
				else:
					self._cur_ch_idx += 1
					tok = Token(Token.STRING, self._prog_src[tok_begin:self._cur_ch_idx])
					print(tok.word)
					print(tok.part_of_speech)
					return tok
			elif ch in Scanner.OPERATORS:
				return self._consume_until(tok_begin, Scanner.OPERATORS, Token.OPERATOR)
			elif ch in Scanner.DIGITS:
				return self._consume_until(tok_begin, Scanner.DIGITS, Token.DIGIT)
			elif ch in Scanner.ALPHAS:
				return self._consume_until(tok_begin, Scanner.ALPHAS+Scanner.DIGITS, Token.ALPHA)
		
		except IndexError:
			return None
		return ch

if __name__ == "__main__":
	s = Scanner(sys.argv[1]);
	while s.next_token():
		pass
