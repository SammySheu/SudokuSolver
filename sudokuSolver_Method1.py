import time
from printBoard import printBoard

class Solution:
    def solveSudoku(self, board: list[list[str]]) -> None:
        # print('\n\n\n\n\n\n\n\n\n\n\n\n\n')
        # printBoard(board)
        def dfs(r, c):
            # printBoard(board)
            if r>=8 and c>=9:               # Depth search to the end and return True
                return True
            elif c>=9:                      # From the end of current row to the begin of next row
                r+=1
                c=0

            if str(board[r][c])>='1' and str(board[r][c])<='9':
                return dfs(r, c+1)          # if element has been filled, search next element
            
            for num in range(1,10):
                if self.isSafe(board, r, c, num):
                    board[r][c] = str(num)
                    right = dfs(r, c+1)
                    if right :
                        return True
                    else:
                        board[r][c] = '.'
            return False
        dfs(0,0)
        # printBoard(board)

    def isSafe(self, board, r, c, num):
        def checkByGroup():
            startRow = r - r%3
            startColumn = c - c%3
            for i in range(3):
                for j in range(3):
                    if str(board[startRow + i][startColumn +j]) == str(num):
                                return False
            return True    
        def checkByRow():
            for i in range(9):
                if str(board[r][i]) == str(num):
                    return False
            return True
        def checkByColumn():
            for i in range(9):
                if str(board[i][c]) == str(num):
                    return False
            return True
        return checkByColumn() & checkByGroup() & checkByRow()

    def load_board(self, filename):
        with open(filename, 'r') as f:
            board = [list(line.strip()) for line in f.readlines()]
        return board

from loadBoard import loadBoard
board1 = loadBoard('board1.txt')
board2 = loadBoard('board2.txt')
board3 = loadBoard('board3.txt')


import time
start_time = time.time()
Solution().solveSudoku(board3)
print("Method1 --- %s seconds --- " % (time.time() - start_time))