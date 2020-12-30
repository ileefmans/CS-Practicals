import random 
import numpy as np




class Board:
	def __init__(self):
		self.state = [[None, None, None, None], [None, None, None, None], [None, None, None, None], 
					[None, None, None, None]]

	def update(self, player, collumn):

		row = self.checkspace(collumn)

		if player == 'A':
			self.state[row][collumn] = 'X'
		else:
			self.state[row][collumn] = 'O'




	def checkspace(self, collumn):
		for i in range(1, len(self.state)+1):
			if self.state[-i][collumn] == None:
				return -i
		return False

	def display(self):
		for i in self.state:
			print(i)





def valid_move(collumn, state):
	if collumn not in [0,1,2,3]:
		return False
	if state[0][collumn] != None:
		return False
	else:
		return True


# --------------------------------------------------------------------------
# Winning Move in a 4x4 game

def winning_move(state):
	#horizontal
	tot_count=0
	for i in range(len(state)):
		counth=0
		countv = 0
		for j in range(len(state[i])):

			if (j ==0) and state[i][j]!=None:
				first = state[i][j]
				counth+=1
			elif (j==0) and state[i][j]==None:
				break

			else:
				if state[i][j] ==first:
					counth+=1

		if counth==4:
			tot_count+=counth

	if tot_count>0:
		return True
	


	# vertical
	tot_count=0
	for i in range(len(state)):
		counth=0
		countv = 0
		for j in range(len(state[i])):

			if (j ==0) and state[j][i]!=None:
				first = state[j][i]
				countv+=1
			elif (j==0) and state[j][i]==None:
				break

			else:
				if state[j][i] ==first:
					countv+=1


		if countv==4:
			tot_count+=countv

	if tot_count>0:
		return True



	# diagonal
	


	count = 0
	for i in range(len(state)):
		if (i==0) and state[i][i] != None:
			first = state[i][i]
			count+=1
		elif (i==0) and state[i][i] ==None:
			break
		else:
			if state[i][i]==first:
				count+=1
	if count==4:
		return True


	stateT = np.transpose(np.array(state))
	count = 0
	for i in range(len(stateT)):

		if (i==0) and stateT[i][i] != None:
			first = stateT[i][i]
			count+=1
		elif (i==0) and stateT[i][i] ==None:
			break
		else:
			if stateT[i][i]==first:
				count+=1


	if count==4:
		return True
	else:
		return False


# --------------------------------------------------------------------------




class HumanPlayer:
	def __init__(self, player):
		self.player = player

	def play(self, state):

		valid = False
		while valid == False:
			move = int(input("Enter the collumn you wish to choose, must be in {0, 1, 2, 3}"))

			not_full = valid_move(move, state)
			if (move in [0, 1, 2, 3]) or not_full:
				valid = True
			else:
				print("Please enter a valid collumn number that is not full")

		return move 






class Game:
	def __init__(self):

		self.playerA = HumanPlayer('A')
		self.playerB = HumanPlayer('B')
		self.board = Board()


	def start(self):
		


		count = 0

		while count<16:
			# Display board
			self.board.display()

			# Player A moves
			valid = False
			while valid ==False:	
				moveA = self.playerA.play(self.board.state)
				
				if self.board.checkspace(moveA) == False:
					valid = False
				else:
					valid = True

			self.board.update(self.playerA.player, moveA)
			count+=1


			# check if winning move
			if winning_move(self.board.state):
				self.board.display()
				print("PLAYER A WINS")
				break

			# ---------------------------------------------

			# Display board
			self.board.display()
			# Player B moves

			valid = False
			while valid ==False:
				moveB = self.playerB.play(self.board.state)
				if self.board.checkspace(moveB) == False:
					valid = False
				else:
					valid = True




			self.board.update(self.playerB.player, moveB)
			count+=1

			# check if winning move
			if winning_move(self.board.state):
				self.board.display()
				print("PLAYER B WINS")
				break

		self.board.display()

		print("DONE")





if __name__ == '__main__':
    game = Game()
    game.start()