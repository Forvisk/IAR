from random import randint

class Ant:
	code = 0
	pos = [-0, -0]
	
	def __init__(self, code, pos):
		self.code = code
		self.carry = False
		self.pos = pos