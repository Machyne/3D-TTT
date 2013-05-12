
class Game(object):
	def __init__(self,size):
		self.size = size
		self.s2 = size**2
		self.board = [0 for x in range(size**3)]
		self.currentPlayer = 1


	# num goes from 1 to 27 inclusive
	def numToCoords(self,num):
		num -= 1
		x = num%self.size 
		z = int(num/self.s2)
		y = (num - x - (self.s2*z))/self.size
		return (x+1,y+1,z+1)

	def coordsToNum(self,x,y,z):
		return x+(self.size*y)+(self.s2*z)-self.size-self.s2

	def __repr__(self):
		player = (' ','X','O')
		bs = ''
		dashCount = 2*self.size-1
		for x in range(self.s2):
			spaceCount = dashCount * int(x/self.size)
			bs += (' '*spaceCount) + (('{}|'*self.size)[:-1]) + '\n'
			if (x%self.size) != self.size-1:
				bs += (' '*spaceCount)+('-'*dashCount)+'\n'
			else:
				bs+='\n'
		return bs.format(*[player[x] for x in self.board])
		
	def move(self,x,y,z):
		if(not(x in range(1,self.size+1) and y in range(1,self.size+1) and z in range(1,self.size+1) )):
			return False
		num = self.coordsToNum(x,y,z)-1
		if(self.board[num]!=0):
			return False
		self.board[num] = self.currentPlayer;
		self.currentPlayer = 1 + self.currentPlayer%2
		return True

	def checkWin(self):
		for player in [1,2]:
			coordList = []
			for x in range(self.size**3):
				if(self.board[x]==player):
					coordList.append(self.numToCoords(x+1))
			#print 'coordList',coordList
			l = len(coordList)
			for x in range(l):
				for y in range(x+1,l):
					c1 = coordList[x]
					c2 = coordList[y]
					#print 'examining',c1,'and',c2
					dif = [c2[i]-c1[i] for i in range(3)]
					#print 'dif',dif
					#print 'here:',self.addN(c2,dif,1)
					next = [self.addN(c2,dif,n) for n in range(1,self.size-1)]
					#print 'next',next
					win = True
					for c3 in next:
						if not(c3 in coordList):
							win = False
							break
					if win:
						return player
		return 0

	def addN(self,t,l,n):
		x = [-999999 for x in l]
		for i in range(3):
			x[i] = t[i]+(n*l[i])
		return tuple(x)
						

def main():
	size = int(raw_input("What size board would you like? "))
	g = Game(size);
	while g.checkWin()==0:
		print g
		userStrs = raw_input("Enter Player {}'s move coordinates:\n    ".format(g.currentPlayer)).strip().split(',')
		if(len(userStrs) != 3 ):
			print "Bad input! Enter input in the form x,y,z"
			continue
		moved = g.move(*[int(s) for s in userStrs])
		if(not moved):
			print "Bad move! Only move to open squares, specify values from 1 to {}".format(g.size)
	print g
	print "Game over - player {} wins! :)".format(g.checkWin())


main()
