import random


class Board:
	def __init__(self):

		self.state = [[None, None, None], [None, None, None], [None, None, None]]

	def update(self, player, move):

		dim1 = move[0]
		dim2 = move[1]

		if player == 'A':
			self.state[dim1][dim2] = 'X'
		else:
			self.state[dim1][dim2] = 'O'

	def display(self):
		return ('\n \n \n'+ str(self.state[0])+ '\n' + str(self.state[1]) + '\n' + str(self.state[2]) + '\n \n \n')


def conversion(move):
	conv = {'l': 0, 'c': 1, 'r': 2, 't':0, 'b': 2}
	move1 = conv[move[0]]
	move2 = conv[move[1]]

	return move1, move2


class HumanPlayer:
	def __init__(self):
		self.player = 'A'

	def play(self, prev_moves):

		counter=0
		while counter==0:

			acceptable1 = False
			while acceptable1==False:
				move_row = input("Please enter desired row 't' for top, 'c' for center, 'b' for bottom'")
				if move_row in ['t', 'c', 'b']:
					acceptable1 = True
				else:
					print("Please input row in correct format")


			acceptable2 = False
			while acceptable2==False:
				move_collumn = input("Please enter desired collumn 'l' for left, 'c' for center, 'r' for right'")
				if move_collumn in ['l', 'c', 'r']:
					acceptable2 = True
				else:
					print("Please input collumn in correct format")

			move = (move_row, move_collumn)
			move = conversion(move)

			if move in prev_moves:
				print("SPOT TAKEN PLAY AGAIN")
			else:
				counter+=1

		return move



class Agent:
	def __init__(self):

		self.player = 'B'
	def play(self, prev_moves):

		counter=0
		while counter==0:
			move_row = random.randrange(3)
			move_collumn = random.randrange(3)

			move = (move_row, move_collumn)

			if move in prev_moves:
				pass
			else:
				counter+=1
		return move


def winner(board_state):
	done = False
	if board_state[0][0] == board_state[0][1] == board_state[0][2]!=None:
		done = True
	if board_state[1][0] == board_state[1][1] == board_state[1][2]!=None:
		done = True
	if board_state[2][0] == board_state[2][1] == board_state[2][2]!=None:
		done = True
	if board_state[0][0] == board_state[1][0] == board_state[2][0]!=None:
		done = True
	if board_state[0][1] == board_state[1][1] == board_state[2][1]!=None:
		done = True
	if board_state[0][2] == board_state[1][2] == board_state[2][2]!=None:
		done = True
	if board_state[0][0] == board_state[1][1] == board_state[2][2]!=None:
		done = True
	return done






class TicTacToe:

	def __init__(self):
		self.board = Board()


	def print_board(self):
		print(self.board.display())



	def one_game(self, first='A'):

		prev_moves = []
		count = 0

		
		if first == 'A':
			player1 = HumanPlayer()
			player2 = Agent()
		else:
			player1 = Agent()
			player2 = HumanPlayer()

			# ------- First player --------------

		while count<9:			
			move1 = player1.play(prev_moves)

			prev_moves.append(move1)

			self.board.update(player1.player, move1)
			self.print_board()

			if winner(self.board.state):
				print("PLAYER A WINS")
				break

			# ---------- Second player ------------

			move2 = player2.play(prev_moves)

			prev_moves.append(move2)

			self.board.update(player2.player, move2)

			print("AGENT HAS MOVED")
			self.print_board()

			count+=1

			if winner(self.board.state):
				print("PLAYER B WINS")
				break
			if count==9:
				break

		self.print_board()
		print("DONE")

	def play_game(self):
		keep_playing=True
		while keep_playing:
			self.one_game()

			
			keep_playing = input('DO YOU WANT TO PLAY AGAIN (True/False)')
			self.board.state = [[None, None, None], [None, None, None], [None, None, None]]
				




if __name__ == "__main__":

    game = TicTacToe()
    game.print_board()
  
    game.play_game()
    


    # Board = Board()
    # print(Board.display())

    # playerA = HumanPlayer()
    # print(playerA.play())
    # agent = Agent()
    # print(agent.play([(1,2), (2,0)]))






