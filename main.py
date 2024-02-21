# sourcery skip: use-itertools-product
import pygame
import numpy
import math
import time
pygame.init()

WIDTH, HEIGHT, BLOCKSIZE = 1000, 800, 40
# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True


cellArray = numpy.zeros((HEIGHT//BLOCKSIZE-1,WIDTH//BLOCKSIZE))


runLife = False
def displayBoard(board):
    screen.fill("black")
    for rown,row in enumerate(board,1):
        for celln,cell in enumerate(row):
            if cell == 0:
                pygame.draw.rect(screen,"black",(celln*BLOCKSIZE,rown*BLOCKSIZE,BLOCKSIZE,BLOCKSIZE))
            else:
                pygame.draw.rect(screen,"green",(celln*BLOCKSIZE,rown*BLOCKSIZE,BLOCKSIZE,BLOCKSIZE))

    for i in range(0,WIDTH,BLOCKSIZE):
        pygame.draw.line(screen,"white",(i,BLOCKSIZE),(i,HEIGHT))
    for i in range(BLOCKSIZE,HEIGHT,BLOCKSIZE):
        pygame.draw.line(screen,"white",(0,i),(WIDTH,i))
    if runLife:
        pygame.draw.rect(screen,"white",pygame.Rect(0.2*BLOCKSIZE,0,0.2*BLOCKSIZE,BLOCKSIZE))
        pygame.draw.rect(screen,"white",pygame.Rect(0.6*BLOCKSIZE,0,0.2*BLOCKSIZE,BLOCKSIZE))
    else:
        pygame.draw.polygon(screen, "white",(
                        ((1 - (0.5/math.tan(math.radians(30)))) * BLOCKSIZE,0* BLOCKSIZE),
                        ((1 - (0.5/math.tan(math.radians(30)))) * BLOCKSIZE,1* BLOCKSIZE),
                        (1 * BLOCKSIZE,0.5* BLOCKSIZE) ))
def processBoard(board:numpy.ndarray):
    board = numpy.pad(board,(1,1),mode = 'constant')
    newBoard = board.copy()
    for rown in range(1,len(board)-1):
        for celln in range(1,len(board)-1):
            neighbors = [board[celln-1,rown-1],board[celln,rown-1],board[celln+1,rown-1],board[celln-1,rown],board[celln+1,rown],board[celln-1,rown+1],board[celln,rown+1],board[celln+1,rown+1]]
            if sum(neighbors) < 2 or sum(neighbors) > 3:
                newBoard[celln,rown] = 0
            elif sum(neighbors) == 3 and board[celln,rown] == 0:
                newBoard[celln,rown] = 1
    return newBoard[1:-1,1:-1]
    
pygame.time.set_timer(pygame.USEREVENT, 500)
displayBoard(cellArray)   
while running:
    
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            topX = mouseX//BLOCKSIZE
            topY = mouseY//BLOCKSIZE -1
            print((mouseX,mouseY))  
            print((topX,topY))
            if  topY == -1:
                if topX == 0:
                    runLife = not runLife
            else:
                cellArray[topY][topX] = 1 if cellArray[topY][topX] == 0 else 0
        if event.type == pygame.USEREVENT and runLife:
            cellArray = processBoard(cellArray)
        displayBoard(cellArray)
    
    
    # fill the screen with a color to wipe away anything from last frame
    

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()