import numpy as np
import random
import pygame
import sys
import math

colorBlue = (0,0,255)
colorBlack = (0,0,0)
colorRed = (255,0,0)
colorYellow = (255,255,0)

rowCount = 6
columnCount = 7

player = 0
ai = 1

empty = 0
playerPiece = 1
aiPiece = 2

windowLength = 4

def createBoard():
	board = np.zeros((rowCount,columnCount))
	return board

def dropPiece(board, row, col, piece):
	board[row][col] = piece

def isValidLocation(board, col):
	return board[rowCount-1][col] == 0

def getNextOpenRow(board, col):
	for r in range(rowCount):
		if board[r][col] == 0:
			return r

def printBoard(board):
	print(np.flip(board, 0))

def winningMove(board, piece):
	for c in range(columnCount-3):
		for r in range(rowCount):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	for c in range(columnCount):
		for r in range(rowCount-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	for c in range(columnCount-3):
		for r in range(rowCount-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	for c in range(columnCount-3):
		for r in range(3, rowCount):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def evaluateWindow(window, piece):
	score = 0
	oppPiece = playerPiece
	if piece == playerPiece:
		oppPiece = aiPiece

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(empty) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(empty) == 2:
		score += 2

	if window.count(oppPiece) == 3 and window.count(empty) == 1:
		score -= 4

	return score

def scorePosition(board, piece):
	score = 0

	centerArray = [int(i) for i in list(board[:, columnCount//2])]
	centerCount = centerArray.count(piece)
	score += centerCount * 3

	for r in range(rowCount):
		rowArray = [int(i) for i in list(board[r,:])]
		for c in range(columnCount-3):
			window = rowArray[c:c+windowLength]
			score += evaluateWindow(window, piece)

	for c in range(columnCount):
		colArray = [int(i) for i in list(board[:,c])]
		for r in range(rowCount-3):
			window = colArray[r:r+windowLength]
			score += evaluateWindow(window, piece)

	for r in range(rowCount-3):
		for c in range(columnCount-3):
			window = [board[r+i][c+i] for i in range(windowLength)]
			score += evaluateWindow(window, piece)

	for r in range(rowCount-3):
		for c in range(columnCount-3):
			window = [board[r+3-i][c+i] for i in range(windowLength)]
			score += evaluateWindow(window, piece)

	return score

def isTerminalNode(board):
	return winningMove(board, playerPiece) or winningMove(board, aiPiece) or len(getValidLocations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
	validLocations = getValidLocations(board)
	isTerminal = isTerminalNode(board)
	if depth == 0 or isTerminal:
		if isTerminal:
			if winningMove(board, aiPiece):
				return (None, 100000000000000)
			elif winningMove(board, playerPiece):
				return (None, -10000000000000)
			else:
				return (None, 0)
		else:
			return (None, scorePosition(board, aiPiece))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(validLocations)
		for col in validLocations:
			row = getNextOpenRow(board, col)
			bCopy = board.copy()
			dropPiece(bCopy, row, col, aiPiece)
			newScore = minimax(bCopy, depth-1, alpha, beta, False)[1]
			if newScore > value:
				value = newScore
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else:
		value = math.inf
		column = random.choice(validLocations)
		for col in validLocations:
			row = getNextOpenRow(board, col)
			bCopy = board.copy()
			dropPiece(bCopy, row, col, playerPiece)
			newScore = minimax(bCopy, depth-1, alpha, beta, True)[1]
			if newScore < value:
				value = newScore
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

def getValidLocations(board):
	validLocations = []
	for col in range(columnCount):
		if isValidLocation(board, col):
			validLocations.append(col)
	return validLocations

def pickBestMove(board, piece):

	validLocations = getValidLocations(board)
	bestScore = -10000
	bestCol = random.choice(validLocations)
	for col in validLocations:
		row = getNextOpenRow(board, col)
		tempBoard = board.copy()
		dropPiece(tempBoard, row, col, piece)
		score = scorePosition(tempBoard, piece)
		if score > bestScore:
			bestScore = score
			bestCol = col

	return bestCol

def drawBoard(board):
	for c in range(columnCount):
		for r in range(rowCount):
			pygame.draw.rect(screen, colorBlue, (c*squareSize, r*squareSize+squareSize, squareSize, squareSize))
			pygame.draw.circle(screen, colorBlack, (int(c*squareSize+squareSize/2), int(r*squareSize+squareSize+squareSize/2)), RADIUS)
	
	for c in range(columnCount):
		for r in range(rowCount):		
			if board[r][c] == playerPiece:
				pygame.draw.circle(screen, colorRed, (int(c*squareSize+squareSize/2), height-int(r*squareSize+squareSize/2)), RADIUS)
			elif board[r][c] == aiPiece: 
				pygame.draw.circle(screen, colorYellow, (int(c*squareSize+squareSize/2), height-int(r*squareSize+squareSize/2)), RADIUS)
	pygame.display.update()

board = createBoard()
printBoard(board)
gameOver = False

pygame.init()

squareSize = 125

width = columnCount * squareSize
height = (rowCount+1) * squareSize

size = (width, height)

RADIUS = int(squareSize/2 - 5)

screen = pygame.display.set_mode(size)
drawBoard(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(player, ai)

while not gameOver:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, colorBlack, (0,0, width, squareSize))
			posx = event.pos[0]
			if turn == player:
				pygame.draw.circle(screen, colorRed, (posx, int(squareSize/2)), RADIUS)

		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, colorBlack, (0,0, width, squareSize))
			if turn == player:
				posx = event.pos[0]
				col = int(math.floor(posx/squareSize))

				if isValidLocation(board, col):
					row = getNextOpenRow(board, col)
					dropPiece(board, row, col, playerPiece)

					if winningMove(board, playerPiece):
						label = myfont.render("Jogador 1 vence!!", 1, colorRed)
						screen.blit(label, (40,10))
						gameOver = True

					turn += 1
					turn = turn % 2

					printBoard(board)
					drawBoard(board)


	if turn == ai and not gameOver:				

		col, minimaxScore = minimax(board, 5, -math.inf, math.inf, True)

		if isValidLocation(board, col):
			row = getNextOpenRow(board, col)
			dropPiece(board, row, col, aiPiece)

			if winningMove(board, aiPiece):
				label = myfont.render("Jogador 2 vence!!", 1, colorYellow)
				screen.blit(label, (40,10))
				gameOver = True

			printBoard(board)
			drawBoard(board)

			turn += 1
			turn = turn % 2

	if gameOver:
		pygame.time.wait(3000)