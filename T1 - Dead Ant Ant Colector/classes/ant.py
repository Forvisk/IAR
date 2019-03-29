from random import randint
import threading
import time

exitFlag = 0

class Ant (threading.Thread):
	code = 0
	pos = [ 0, 0]
	nextmove = [ 1, 1]
	carry = False
	
	def __init__(self, threadID, pos):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.pos = pos

	def run(self):
		print( 'Iniciando ', self.threadID)
		#print_time( self.threadID, 3, 1)
		self.move()
		print( 'finalizando ', self.threadID)

	def move( self):
		#lock ambiente
		ambiente[ self.pos[0]][ self.pos[1]] -= 2
		self.pos[0] += self.nextmove[0]
		self.pos[1] += self.nextmove[1]
		print( self.pos)
		ambiente[ self.pos[0]][ self.pos[1]] += 2
		#unlockambiente



def print_time( threadID, counter, delay):
		while counter:
			if exitFlag:
				threadName.exit()
			time.sleep(delay)
			print( threadID, ' - ', time.ctime( time.time()))
			counter -= 1