def move(board, pocket, stealing=True):
   
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

def isValidMove(board, pocket):
    return board[pocket] != 0
     
def minimax(board, player, stealing, depth, alpha, beta, maximizingPlayer):
	
    #check if there are no moves possible
    
    winningPlayer = winner(board)
    if (winningPlayer != 0):
        board = endgame(board)
        return score(board, player)
    
    if(depth == 0):
        return score(board, player)
    
    if(player == 1):
        playerPockets = range(6)
    
    if(player == 2):
        playerPockets = range(6)+7
    
    if (maximizingPlayer):
        maxScore = float('-inf')
        for pocket in playerPockets:
            if(isValidMove(board, pocket)):
                childBoard, nextPlayer = move(board, pocket, stealing)
                
                if(nextPlayer == player): # if player gets another move then next turn is maximizer player's trun
                    childScore, _ = minimax(childBoard, nextPlayer, stealing, depth, alpha, beta, True)
                
                else: # else The next trun is minimizer player's trun
                    childScore, _ = minimax(childBoard, nextPlayer, stealing, depth, alpha, beta, False)
                
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
                    childScore, _ = minimax(childBoard, nextPlayer, stealing, depth, alpha, beta, False)
                
                else: # else The next trun is minimizer player's trun
                    childScore, _ = minimax(childBoard, nextPlayer, stealing, depth, alpha, beta, True)
            
                if(childScore < minScore):
                    nextMove = pocket
                    minScore = childScore
                    
                if(childScore < beta):
                    beta = childScore
                    
                if (beta <= alpha):
                    break
                return minScore, nextMove
        

def nextPlay(board, player, stealing=True):
    minimax(board, player, stealing, 3, float('-inf'), float('inf'), True)
    
### to be implemented
def score(board, player): 
    return
def winner(board): 
    return
def endgame(board): 
    return
