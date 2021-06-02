initialBoard = [4,4,4,4,4,4, 0,    4,4,4,4,4,4, 0]
pocketNames = ['f','e','d','c','b','a', 0,    'a','b','c','d','e','f', 0]      
import time
import  pickle
import os
#os.system("cls")

def Save(board,player,stealing,path):
    with open(path,'wb')as f:
        pickle.dump([board,player,stealing],f)
    return
    

def Load(path):
    with open(path,'rb')as f:
        board,player,stealing=pickle.load(f)
    return board,player,stealing


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

def minimax(board, player, stealing, depth, alpha, beta, maximizingPlayer):
	
    #check if time limit is reached
    # print(start_limit_list)
    if (start_limit_list[1] != -1 and (time.time() - start_limit_list[0]) > start_limit_list[1]):
        return score(board, player), -1
    
    # #check if a key is pressed
    # if(flag_list):
    #     return score(board, player), -1
    
    #check if there are no moves possible
    winningPlayer, board = findWinner(board)
    
    if (winningPlayer != 0):
        if(maximizingPlayer):
            return score(board, player), -1
        else:
            if(player==1):
                return score(board, 2), -1
            else:
                return score(board, 1), -1
    
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
                # print(board, pocket)
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
                # print(board, pocket)
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

start_limit_list = [0,-1]

def bestPocket(board, player, stealing=True, depth=10):
    # print("loading...\nPress Ctrl-C to terminate (time limit is", start_limit_list[1], "seconds)",end='\r')
    start_limit_list[0] = time.time()
    maxScore = float('-inf')
    try:
        for depth in range(1,15):
            Score, Move = minimax(board, player, stealing, depth, float('-inf'), float('inf'), True)
            if (Score > maxScore):
                nextMove = Move
                maxScore = Score
                # print(nextMove)
            
    except KeyboardInterrupt:
        print("\nCtrl-C is pressed",end='\r')
        
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


## Time analysis

import time
for depth in range(14):
    board = initialBoard
    start_time = time.time()
    print('at depth',depth,'the best pocket is', bestPocket(board, 1, True, depth))
    print( "it took", (time.time() - start_time), "seconds\n\n")

'''

def display(board,x):
    W  = '\033[0m'
    R  = '\033[31m' # red
    G  = '\033[32m' # green
    P  = '\033[35m' # purple
    print('')
    if(x==0):
        print(P+"\t\t\t\t"+"   Player1".expandtabs(30))
        print(G+"\t\t\t"+'a'+'\t'+'b'+'\t'+'c'+'\t'+'d'+'\t'+'e'+'\t'+'f'.expandtabs(30))
        print(P+"\t\t\t"+str(board[5])+'\t'+str(board[4])+'\t'+str(board[3])+'\t'+str(board[2])+'\t'+str(board[1])+'\t'+str(board[0]).expandtabs(30))
        print(P+"\n\t"+str(board[6])+R+"\t\t\t\t\t\t\t\t"+'\t'+str(board[13]).expandtabs(30))
        print(R+"\n\t\t\t"+str(board[7])+'\t'+str(board[8])+'\t'+str(board[9])+'\t'+str(board[10])+'\t'+str(board[11])+'\t'+str(board[12]).expandtabs(30))
        print(G+"\t\t\t"+'a'+'\t'+'b'+'\t'+'c'+'\t'+'d'+'\t'+'e'+'\t'+'f'.expandtabs(30))
        print(R+"\t\t\t\t"+"   Player2".expandtabs(30)+W)
    elif(x==1):
        print(P+"\t\t\t\t"+"    Player".expandtabs(30))
        print(G+"\t\t\t"+'a'+'\t'+'b'+'\t'+'c'+'\t'+'d'+'\t'+'e'+'\t'+'f'.expandtabs(30))
        print(P+"\t\t\t"+str(board[5])+'\t'+str(board[4])+'\t'+str(board[3])+'\t'+str(board[2])+'\t'+str(board[1])+'\t'+str(board[0]).expandtabs(30))
        print(P+"\n\t"+str(board[6])+R+"\t\t\t\t\t\t\t\t"+'\t'+str(board[13]).expandtabs(30))
        print(R+"\n\t\t\t"+str(board[7])+'\t'+str(board[8])+'\t'+str(board[9])+'\t'+str(board[10])+'\t'+str(board[11])+'\t'+str(board[12]).expandtabs(30))
        print(G+"\t\t\t"+'a'+'\t'+'b'+'\t'+'c'+'\t'+'d'+'\t'+'e'+'\t'+'f'.expandtabs(30))
        print(R+"\t\t\t\t"+"   Computer".expandtabs(30)+W)  
    elif(x==2):
        print(P+"\t\t\t\t"+"   Computer".expandtabs(30)) 
        print(G+"\t\t\t"+'a'+'\t'+'b'+'\t'+'c'+'\t'+'d'+'\t'+'e'+'\t'+'f'.expandtabs(30))
        print(P+"\t\t\t"+str(board[5])+'\t'+str(board[4])+'\t'+str(board[3])+'\t'+str(board[2])+'\t'+str(board[1])+'\t'+str(board[0]).expandtabs(30))
        print(P+"\n\t"+str(board[6])+R+"\t\t\t\t\t\t\t\t"+'\t'+str(board[13]))
        print(R+"\n\t\t\t"+str(board[7])+'\t'+str(board[8])+'\t'+str(board[9])+'\t'+str(board[10])+'\t'+str(board[11])+'\t'+str(board[12]).expandtabs(30))
        print(G+"\t\t\t"+'a'+'\t'+'b'+'\t'+'c'+'\t'+'d'+'\t'+'e'+'\t'+'f'.expandtabs(30))
        print(R+"\t\t\t\t"+"    Player".expandtabs(30)+W)
    return

def getInput(board,player):
    display(board,player)
    user_ip=input("Choose the location of the pocket to play: ")#'a, b, c, d, e, f': " )
    index=9999
    while(1):   
        if(player==1):
            if(user_ip=='a'):
                index=5
            elif (user_ip=='b'):
                index=4
            elif (user_ip=='c'):
                index=3
            elif (user_ip=='d'):
                index=2
            elif (user_ip=='e'):
                index=1
            elif (user_ip=='f'):
                index=0
        elif(player==2):
            if(user_ip=='a'):
                index=7
            elif (user_ip=='b'):
                index=8
            elif (user_ip=='c'):
                index=9
            elif (user_ip=='d'):
                index=10
            elif (user_ip=='e'):
                index=11
            elif (user_ip=='f'):
                index=12
        if(user_ip!='a' and user_ip!='b' and user_ip!='c' and user_ip!='d' and user_ip!='e' and user_ip!='f' ):
            user_ip=input("Enter the right pocket: ")
            continue
        elif(board[index]==0 ):
            user_ip=input("Enter the right pocket: ")
            
        else:
            return index        #pocket
        # print(W)
    return

def inputStealing():
    stealing=None
    while (stealing==None):
        x = input('game mode: stealing y/n? ')
        if(x == 'y'):
            stealing=True
        elif(x == 'n'):
            stealing=False
        else:
            print("invalid input")
    return stealing

def inputPlaying():
    Playing=None
    while (Playing==None):
        x = input('do you want to play the computer y/n? ')
        if(x == 'y'):
            Playing=True
        elif(x == 'n'):
            Playing=False
        else:
            print("invalid input")
    return Playing
    
def inputPlayerNumber():
    while (True):
        x = input('do you want to play first y/n? ')
        if(x == 'y'):
            return 1, 2
        elif(x == 'n'):
            return 2, 1
        else:
            print("invalid input")
    return

def inputimeLimit():
    flag=False
    while (flag==False):
        x = input('do you want to change time limit (20 seconds per move) y/n? ')
        if(x == 'n'):
            return 20
        elif(x == 'y'):
            flag = True
        else:
            print("invalid input")

    timeLimit=None
    while (timeLimit==None):
        x = input('enter time limit: ')
        try:
            x = int(x)
            if(x > 0):
                timeLimit = x
            else:
                print("invalid input")
        except:
            print("invalid input")
            
    
    return timeLimit

def playerVScomputer():
    stealing = inputStealing()
    board = initialBoard
    userPlayer, computerPlayer = inputPlayerNumber()
    player = 1
    
    while(True):
        if(player == userPlayer):
            pocket = getInput(board, player)
            board, player = move(board, pocket, stealing)
            if(player != userPlayer):
                display(board, userPlayer)
        else:
            pocket = bestPocket(board, player, stealing)
            board, player = move(board, pocket, stealing)
            print('\ncomputer played pocket', pocketNames[pocket])
            if(player != userPlayer):
                display(board, userPlayer)
            
        winner, board = findWinner(board)
        if(winner != 0): #display final board
            display(board, userPlayer)
        
        if(winner == userPlayer):
            print('you win')
            break
        elif(winner == computerPlayer):
            print('computer wins')
            break
        elif(winner == 3):
            print('a tie')
            break
    return

def computerVScomputer():
    stealing = inputStealing()
    board = initialBoard
    display(board,0)
    player=1
    while(True):
        pocket = bestPocket(board, player, stealing)
        print('\nplayer',player,'plays pocket', pocketNames[pocket])
        board, player = move(board, pocket, stealing)
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

playing = inputPlaying()
timeLimit = inputimeLimit()
start_limit_list[1] = timeLimit
if(playing):
    playerVScomputer()

else:
    computerVScomputer()

