initialBoard = [4,4,4,4,4,4, 0,    4,4,4,4,4,4, 0]
depth=8
def move(board, pocket, stealing=True):
    
    board=board.copy()
    # determine which player is playing
    
    if(pocket<6):
        player = 1
        nextPlayer=2
    else:
        player = 2
        nextPlayer=1
    
    # move stones from current pocket
    
    stones = board[pocket]
    board[pocket] = 0
    skipped=0
    for i in range(pocket+1, pocket+stones+1):
        currentPocket = (i + skipped) % 14
        skip = False
        if((currentPocket == 6 and player == 2) or (currentPocket == 13 and player == 1)):
             skip=True
        
        if skip:
            board[(currentPocket+1) % 14] = board[(currentPocket+1) % 14] + 1
            skipped = skipped + 1
            currentPocket = (currentPocket + 1) % 14
        else:
            board[currentPocket] = board[currentPocket] + 1
    
    # stealing
    
    if (stealing):
        if(board[currentPocket] == 1 and ((player == 1 and currentPocket<6) 
                                          or (player == 2 and currentPocket>6 and currentPocket<13))):
            
            if(player==1):
                mancala=6
            elif(player==2):
                mancala=13
                
            board[mancala]=board[mancala] + 1 + board[12 - currentPocket]
            board[currentPocket]=0
            board[12 - currentPocket]=0
    
    #  if a player ended at his mancala he plays again
    
    if (player == 1 and currentPocket == 6):
        nextPlayer = 1
    
    elif (player == 2 and currentPocket == 13):
        nextPlayer = 2
    
    return board, nextPlayer

'''
board=[1,0,0,0,0,0, 0,    0,0,0,0,0,0, 0]
board, nextPlayer = move(board, pocket=0, stealing=False)
print(board)
print ('next player is', nextPlayer)

board=[0,0,0,0,0,0, 0,    0,0,0,0,0,3, 0]
board, nextPlayer = move(board, pocket=12, stealing=False)
print(board)
print ('next player is', nextPlayer)

board=[0,0,0,0,0,9, 0,    0,0,0,0,0,0, 0]
board, nextPlayer = move(board, pocket=5, stealing=False)
print(board)
print ('next player is', nextPlayer)

# hard

board=[0,0,0,0,10,0, 0,    0,0,0,0,0,0, 0]
board, nextPlayer = move(board, pocket=4)
print(board)
print ('next player is', nextPlayer)

board=[0,1,0,0,10,0, 0,    0,0,0,0,0,0, 0]
board, nextPlayer = move(board, pocket=4)
print(board)
print ('next player is', nextPlayer)

board=[0,0,0,0,10,0, 0,    0,0,0,0,0,0, 0]
board, nextPlayer = move(board, pocket=4, stealing=False)
print(board)
print ('next player is', nextPlayer)

board=[0, 0, 0, 0, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0]
board, nextPlayer = move(board, pocket=7, stealing=True)
print(board)
print ('next player is', nextPlayer)

board = [0, 9, 1, 8, 6, 8, 8, 6, 3, 6, 2, 2, 4, 1]
board, nextPlayer = move(board, pocket=5, stealing=True)
print(board)
print ('next player is', nextPlayer)

'''

def isValidMove(board, pocket):
    return board[pocket] != 0
     
def minimax(board, player, stealing, depth, alpha, beta, maximizingPlayer):
	
    #check if there are no moves possible
    
    winningPlayer, board = findWinner(board)
    
    if (winningPlayer != 0):
        return score(board, player), -1
    
    if(depth == 0):
        return score(board, player), -1
    
    if(player == 1):
        playerPockets = range(6)
    
    if(player == 2):
        playerPockets = range(7, 13)
    
    if (maximizingPlayer):
        maxScore = float('-inf')
        for pocket in playerPockets:
            if(isValidMove(board, pocket)):
                childBoard, nextPlayer = move(board, pocket, stealing)
                
                if(nextPlayer == player): # if player gets another move then next turn is maximizer player's trun
                    childScore, _ = minimax(childBoard, nextPlayer, stealing, depth-1, alpha, beta, True)
                
                else: # else The next trun is minimizer player's trun
                    childScore, _ = minimax(childBoard, nextPlayer, stealing, depth-1, alpha, beta, False)
                
                if(childScore > maxScore):
                    nextMove = pocket
                    maxScore = childScore
                
                if(childScore > alpha):
                    alpha = childScore
                    
                if (beta <= alpha):
                    break
        
        return maxScore, nextMove
 
    else:
        minScore = float('inf')
        for pocket in playerPockets:
            if(isValidMove(board, pocket)):
                childBoard, nextPlayer = move(board, pocket)
                
                if(nextPlayer == player): # if player gets anothrt move then next node is minimizer also
                    childScore, _ = minimax(childBoard, nextPlayer, stealing, depth-1, alpha, beta, False)
                
                else: # else The next trun is minimizer player's trun
                    childScore, _ = minimax(childBoard, nextPlayer, stealing, depth-1, alpha, beta, True)
            
                if(childScore < minScore):
                    nextMove = pocket
                    minScore = childScore
                    
                if(childScore < beta):
                    beta = childScore
                    
                if (beta <= alpha):
                    break
        return minScore, nextMove
        
def bestPocket(board, player, stealing=True):
    maxScore, nextMove = minimax(board, player, stealing, depth, float('-inf'), float('inf'), True)
    return nextMove#, maxScore

'''
board=[1,0,0,0,2,1, 0,    1,0,0,0,0,0, 0]
print(bestPocket(board, 1))

board=[1,0,0,3,1,0, 0,    1,0,0,0,0,0, 0]
print(bestPocket(board, 1))

board=[1,0,0,3,0,1, 0,    1,0,0,0,0,0, 0]
print(bestPocket(board, 1))



board=[0,0,0,0,2,1, 0,    1,0,0,0,0,0, 0]
print(bestPocket(board, 1))

board=[0,0,0,3,1,0, 0,    1,0,0,0,0,0, 0]
print(bestPocket(board, 1))



board=[1,0,0,3,0,1, 0,    1,0,0,0,0,0, 0]
print(bestPocket(board, 1))
board, nextPlayer = move(board, pocket=0)
board, nextPlayer = move(board, pocket=7)
print(board)
board=[0, 0, 0, 3, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1]
print(bestPocket(board, 1))
'''
    
def score(board, player): 
    if(player==1):
        return board[6]-board[13]
    else:
        return board[13]-board[6]
    
def findWinner(board):
    result = 0
    if(board[0]==board[1]==board[2]==board[3]==board[4]==board[5]==0 ):

        board[13]+=board[7]+board[8]+board[9]+board[10]+board[11]+board[12]
        board[7]=0
        board[8]=0
        board[9]=0
        board[10]=0
        board[11]=0
        board[12]=0
    elif(board[7]==board[8]==board[9]==board[10]==board[11]== board[12]==0 ):
    
        board[6]+=board[0]+board[1]+board[2]+board[3]+board[4]+board[5]
        board[0]=0
        board[1]=0
        board[2]=0
        board[3]=0
        board[4]=0
        board[5]=0
    else:
        return result,board
    
    if(board[6]>board[13]):
        result=1
    elif(board[13]>board[6]):
        result =2
    elif(board[13]==board[6]): 
        result =3
    else:
        result =0
    
    
    
    return result, board

def play():
    board = initialBoard
    display(board,0)
    player=1
    while(True):
        pocket = bestPocket(board, player)
        print('player',player,'plays pocket', pocket+1)
        board, player = move(board, pocket)
        winner, board = findWinner(board)
        display(board, 0)
        if(winner==1):
            print('player 1 wins')
            break
        elif(winner==2):
            print('player 2 wins')
            break
        elif(winner==3):
            print('a tie')
            break

def display(board, x):
	W  = '\033[0m'  # white (normal)
	R  = '\033[31m' # red
	G  = '\033[32m' # green
	O  = '\033[33m' # orange
	B  = '\033[34m' # blue
	P  = '\033[35m' # purple
	C  = '\033[36m' # purple
	if(x==0):
        print(P+"\t\t\t\t Player 1")
        print(P+"\n\t\t\t"+str(board[5])+"  "+str(board[4])+"  "+str(board[3])+"   "+str(board[2])+"   "+str(board[1])+"   "+str(board[0]))
        print(P+"\n\t"+str(board[6])+R+"\t\t\t\t\t\t\t\t"+str(board[13]))
        print(R+"\n\t\t\t"+str(board[7])+"  "+str(board[8])+"  "+str(board[9])+"  "+str(board[10])+"  "+str(board[11])+"  "+str(board[12]))
        print(R+"\n\t\t\t\t Player 2")
    elif(x==1):
        print(P+"\t\t\t\t Player")
        print(G+"\t\t\t"+'a'+"  "+'b'+"  "+'c'+"   "+'d'+"   "+'e'+"   "+'f')
        print(P+"\t\t\t"+str(board[5])+"  "+str(board[4])+"  "+str(board[3])+"   "+str(board[2])+"   "+str(board[1])+"   "+str(board[0]))
        print(P+"\n\t"+str(board[6])+R+"\t\t\t\t\t\t\t\t"+str(board[13]))
        print(R+"\n\t\t\t"+str(board[7])+"  "+str(board[8])+"  "+str(board[9])+"  "+str(board[10])+"  "+str(board[11])+"  "+str(board[12]))
        print(R+"\n\t\t\t\t Computer")  
        print(W+"\n\n"+"Choose the location of the pocket to play: 'a, b, c, d, e, f': " )
    elif(x==2):
        print(P+"\t\t\t\t Computer")
        print(P+"\t\t\t"+str(board[5])+"  "+str(board[4])+"  "+str(board[3])+"   "+str(board[2])+"   "+str(board[1])+"   "+str(board[0]))
        print(P+"\n\t"+str(board[6])+R+"\t\t\t\t\t\t\t\t"+str(board[13]))
        print(R+"\n\t\t\t"+str(board[7])+"  "+str(board[8])+"  "+str(board[9])+"  "+str(board[10])+"  "+str(board[11])+"  "+str(board[12]))
        print(G+"\t\t\t"+'a'+"  "+'b'+"  "+'c'+"   "+'d'+"   "+'e'+"   "+'f')
        print(R+"\t\t\t\t Player")  
        print(W+"\n\n"+"Choose the location of the pocket to play: 'a, b, c, d, e, f': " )
    return

def getInput(board, player):
    # TODO: checks for invalid input and returns a pocket to play from
    return #pocket

play()

board = initialBoard
display(board,0)
userPlayer = int(input('player 1 or player 2? '))

if(userPlayer == 1):
    computerPlayer = 2
else:
     computerPlayer = 1

player = 1
while(True):
    if(player == userPlayer):
        pocket = getInput(board, player)
        board, player = move(board, pocket)
    else:
        pocket = bestPocket(board, player)
        board, player = move(board, pocket)
        print('computer played pocket', pocket+1)
        if(player != userPlayer):
            display(board, 0)
        
    winner, board = findWinner(board)
    if(winner != 0): #display final board
        display(board, 0)
    
    if(winner == userPlayer):
        print('you win')
        break
    elif(winner == computerPlayer):
        print('computer wins')
        break
    elif(winner == 3):
        print('a tie')
        break



