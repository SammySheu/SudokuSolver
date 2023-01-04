import time
def printBoard(board):
        lineUp = '\033[12A'
        print('', end=lineUp)
        for i in range(9):
            for j in range(3):
                print(' ',board[i][j], end = "")
            print(' ', end='|')
            for j in range(3,6):
                print(' ',board[i][j], end = "")
            print(' ', end='|')
            for j in range(6,9):
                print(' ',board[i][j], end = "")
            print('', end='\n')
            if i==2 or i==5:
                print('  --------+----------+----------')
        print('', end='\n')
        time.sleep(.05)