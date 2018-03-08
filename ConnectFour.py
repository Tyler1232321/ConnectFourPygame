
import pygame
import random
import pickle
import time
import shelve
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PINK = (255,192,203)
YELLOW = (255, 255, 55)


loop = True
#	Selecting Game Mode
while loop == True:
	print("What mode do you want to play?")
	print("A. Two Player")
	print("B. One Player")
	print("C. Computer vs Computer")
	print()
	IN = input("Your Choice? ")
	if IN.upper() == "A":
		gameMode = 2
		loop = False
	elif IN.upper() == "B":
		gameMode = 1
		loop = False
	elif IN.upper() == "C":
		gameMode = 0
		loop = False
	else:
		print("INVALID SELECTION, PLEASE CHOSE AGAIN:")
		print()

# Setup
pygame.init()
 
# Set the width and height of the screen [width,height]
size = [700, 500]
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Hide the mouse cursor
pygame.mouse.set_visible(True)

#	Class for eqach column
class Column():
	#	Initialize the column
	def __init__(self):
		self.height = 400
		self.width = 72
		self.x = 0
		#self.circ = [owner.Empty, owner.Empty, owner.Empty, owner.Empty, owner.Empty, owner.Empty]
		self.circ = [BLACK, BLACK, BLACK, BLACK, BLACK, BLACK]
		self.selected = False

	#	Testing purposes
	def printinfo(self, x):
		self.x = x
		#print(self.x)

	#	Selecting current columns
	def selectcol(self):
		pygame.draw.rect(screen,PINK,[75 + 77*self.x,50, 72,400], 0)		
		for i in range(0, 6):
			pygame.draw.ellipse(screen, self.circ[i], [80+77*self.x, 60+65*i, 67, 55], 0)
		self.selected = True
		pygame.display.flip()

	def unselectcol(self):
		pygame.draw.rect(screen,BLUE, [75+77*self.x, 50, 72, 400], 0)
		for i in range(0, 6):
			pygame.draw.ellipse(screen, self.circ[i], [80+77*self.x, 60+65*i, 67, 55], 0)
		self.selected = False
		pygame.display.flip()

	def dropChip(self, playerColor):
		for i in range(5, -1, -1):
			if self.circ[i] == BLACK:
				self.circ[i] = playerColor
				for i in range(0, 6):
					pygame.draw.ellipse(screen, self.circ[i], [80+77*self.x, 60+65*i, 67, 55], 0)
				pygame.display.flip()
				break
	def canDropChip(self):
		for i in range(5, -1, -1):
			if self.circ[i] == BLACK:
				return True

class Board():
	def __init__(self):
		self.col = [0, 0, 0, 0, 0, 0, 0]
		self.move[7]


#	Check win conditions (Hardest part)
def checkWinConditions(playerToCheck):
	
#	For this function i will be rows and j will be columns
#	Will check win conditions in 4 parts, rows, columns, 
#	diagonal increasing, and diagonal decreasing
	
	#	First check all rows
	for i in range(6):
		win = 0
		for j in range(7):
			if col[j].circ[i] == playerToCheck:
				win +=1
			else:
				win = 0

			if win == 4:
				return True

	#	Now check all Columns
	for j in range(7):
		win = 0
		for i in range(6):
			if col[j].circ[i] == playerToCheck:
				win+=1
			else:
				win = 0

			if win == 4:
				return True

	#	For this part, k is arbitrary index that helps control checking diagonals
	#	Now check diagonals increasing from the bottom left 
	#	Towards top right. This will need to be done in 2 parts
	for k in range(3):
		win = 0
		for j in range(1+k, 7):
			if col[j].circ[6+k-j] == playerToCheck:
				win += 1
			else:
				win = 0

			if win == 4:
				return True
	#	Second part of checking positive diagonals
	for k in range(3):
		win = 0
		for i in range(3+k, -1, -1):
			if col[3+k-i].circ[i] == playerToCheck:
				win += 1
			else:
				win = 0

			if win == 4:
				return True

	#	Start Checking negative diagonals (Staring Along top first)
	for k in range(3):
		win = 0
		for j in range(1+k, 7):
			if col[j].circ[j-k-1] == playerToCheck:
				win += 1
			else:
				win = 0

			if win == 4:
				return True

	#	Negative Diagonals starting along left side
	for k in range(3):
		win = 0
		for i in range(k, 6):
			if col[i-k].circ[i] == playerToCheck:
				win += 1
			else:
				win = 0

			if win == 4:
				return True

	#	Also going to check tying conditions
	tie = True
	for j in range(7):
		for i in range(6):
			if col[j].circ[i] == BLACK:
				tie = False
				return False
	if tie == True:
		displayTieScreen();


def displayTieScreen():
	screen.fill(BLACK)
	pygame.draw.rect(screen,BLUE,[75,50, 532,400], 0)
	for i in range(0, 6):
		for j in range(0, 7):
			pygame.draw.ellipse(screen, col[j].circ[i], [80+77*j, 60+65*i, 67, 55], 0)

	pygame.display.flip()
	gameEnd = True



#	Function to display the winning screen
def displayWin(WinningPlayer):
	screen.fill(WinningPlayer)
	pygame.draw.rect(screen,BLUE,[75,50, 532,400], 0)
	for i in range(0, 6):
		for j in range(0, 7):
			pygame.draw.ellipse(screen, col[j].circ[i], [80+77*j, 60+65*i, 67, 55], 0)

	pygame.display.flip()
	gameEnd = True



class Player():
	def __init__(self):
		self.player = RED

	def switch(self):
		if self.player == RED:
			self.player = YELLOW
		else:
			self.player = RED

currentPlayer = Player()

col = [0, 0, 0, 0, 0, 0, 0]

for i in range(7):
    col[i] = Column()
    col[i].printinfo(i)


screen.fill(WHITE)

pygame.draw.rect(screen,BLUE,[75,50, 532,400], 0)
for i in range(0, 6):
 	for j in range(0, 7):
 		pygame.draw.ellipse(screen, BLACK, [80+77*j, 60+65*i, 67, 55], 0)

if gameMode == 1 or gameMode == 2:
	col[0].selectcol()

gameEnd = False


compWin = False
compLoss = False
# -------- Main Program Loop For Two Players-----------
if gameMode == 2:
	while not done:
		if not gameEnd:
		    for event in pygame.event.get():
		        if event.type == pygame.QUIT:
		            done = True
		            
		            # User pressed down on a key
		        # User let up on a key
		        elif event.type == pygame.KEYDOWN:
		            # If it is an arrow key, reset vector back to zero
		            if event.key == pygame.K_LEFT:
		            	for i in range(6, -1, -1):
		            		if col[i].selected == True and not i == 0:
		            			print("Left key hit")
		            			col[i].unselectcol()
		            			col[i-1].selectcol()
		            			break
		            elif event.key == pygame.K_RIGHT:
		            	for i in range(7):
		            		if col[i].selected == True and not i == 6:
		            			print("Right key hit")
		            			col[i].unselectcol()
		            			col[i+1].selectcol()
		            			break
		            elif event.key == pygame.K_UP:
		            	up = True
		            elif event.key == pygame.K_DOWN:
		                for i in range(7):
		                	if col[i].selected == True:
		                		col[i].dropChip(currentPlayer.player)
		                		if checkWinConditions(currentPlayer.player):
		                			displayWin(currentPlayer.player)
		                			gameEnd = True
		                			
		                		currentPlayer.switch()

	    # Go ahead and update the screen with what we've drawn.
		else:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					done = True


		pygame.display.flip()


	 
	    # Limit frames per second
		clock.tick(60)

	 
	# Close the window and quit.
	pygame.quit()


#	Gonna set some functions for AI Play
def playRandomColumn(currentPlayer):
	played = False
	while not played:
		play = random.randrange(0, 7)
		if col[play].canDropChip():
			col[play].dropChip(currentPlayer)
			played = True
			return play


#	------Main Loop for Computer VS Computer-----------
if gameMode == 0:

    #	AI
	while True and not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
   				done = True
		gameEnd = False
		playRandomColumn(currentPlayer.player)
		if checkWinConditions(currentPlayer.player):
			displayWin(currentPlayer.player)
			gameEnd = True
		currentPlayer.switch()
		time.sleep(.2)
		if gameEnd:
			time.sleep(3)
			screen.fill(WHITE)
			pygame.draw.rect(screen,BLUE,[75,50, 532,400], 0)
			for i in range(0, 6):
			 	for j in range(0, 7):
			 		col[j].circ[i] = BLACK
			 		pygame.draw.ellipse(screen, col[j].circ[i], [80+77*j, 60+65*i, 67, 55], 0)


	pygame.display.flip()
	clock.tick(60)

	pygame.quit()


if gameMode == 1:
    #	Player one goes first
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
   				done = True
		#	If it is the Players turn
		if currentPlayer.player == RED:
			if not compLoss:
				turn = True
			while turn:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
		   				done = True
					# User pressed down on a key
					elif event.type == pygame.KEYDOWN:
					    # If it is an arrow key, reset vector back to zero
					    if event.key == pygame.K_LEFT:
					    	for i in range(6, -1, -1):
					    		if col[i].selected == True and not i == 0:
					    			print("Left key hit")
					    			col[i].unselectcol()
					    			col[i-1].selectcol()
					    			break
					    elif event.key == pygame.K_RIGHT:
					    	for i in range(7):
					    		if col[i].selected == True and not i == 6:
					    			print("Right key hit")
					    			col[i].unselectcol()
					    			col[i+1].selectcol()
					    			break
					    elif event.key == pygame.K_DOWN:
					        for i in range(7):
					        	if col[i].selected == True:
					        		col[i].dropChip(currentPlayer.player)
					        		if checkWinConditions(currentPlayer.player):
					        			displayWin(currentPlayer.player)
					        			compLoss = True
					        			gameEnd = True
					        		turn = False
			currentPlayer.switch()
    	#	If it is the Computer's turn
		elif currentPlayer.player == YELLOW and not gameEnd:
			tempPlay = playRandomColumn(currentPlayer.player)
			# getBoardValue(tempPlay)
			if checkWinConditions(currentPlayer.player):
				displayWin(currentPlayer.player)
				gameEnd = True
			currentPlayer.switch()
			time.sleep(.2)
			if gameEnd:
				time.sleep(3)
				screen.fill(WHITE)
				pygame.draw.rect(screen,BLUE,[75,50, 532,400], 0)
				for i in range(0, 6):
				 	for j in range(0, 7):
				 		col[j].circ[i] = BLACK
				 		pygame.draw.ellipse(screen, col[j].circ[i], [80+77*j, 60+65*i, 67, 55], 0)

	pygame.display.flip()
	clock.tick(60)
	pygame.quit()

pygame.quit()
