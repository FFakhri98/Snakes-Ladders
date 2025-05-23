
import random

round = 0

playerNum =int(input("How many player? "))

if round==0:
    playerPos = [0] * playerNum

board = [0] * 100
boardFin = list(range(100))
for i in range(1,17):
    if i <=8:
        pos = random.randint(1, 98)
        while board[pos] !=0:
            pos = random.randint(1, 98)
            print("the chosen position is: "+str(pos))
        board[pos] = random.randint(5,70)
        while pos+board[pos]>=99 or board[pos+board[pos]]!=0:
            board[pos] = random.randint(5,70)
            print("the ladder is: "+str(board[pos]))
        boardFin[pos] = boardFin[pos] + board[pos]
    else:
        pos = random.randint(1, 98)
        while board[pos] !=0:
            pos = random.randint(1, 98)
            print("the chosen position is: "+str(pos))
        board[pos] = random.randint(-70,-5)
        while pos+board[pos]<=0 or board[pos+board[pos]]!=0:
            board[pos] = random.randint(-70,-5)
            print("the snake is: "+str(board[pos]))
        boardFin[pos] = boardFin[pos] + board[pos]


print(boardFin)
win = 99999
while win == 99999 :
    for p in range(0,playerNum):
        dice = random.randint(1, 6)
        print("player " + str(p) +" is playing.")
        print ("dice is: " + str(dice))
        if playerPos[p]+dice<99 :
            playerPos[p] = playerPos[p] + dice
            if board[playerPos[p]] != 0:
                playerPos[p] = boardFin[playerPos[p]]
            print("its new position is: " + str(playerPos[p]))
        elif playerPos[p]+dice == 99:
            win=p
            print("player " + str(p) +" has won.")
            break
        else:
            print("player " + str(p) +" can't move!")
