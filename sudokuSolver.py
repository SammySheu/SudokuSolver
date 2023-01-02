import time

class Solution:
    def solveSudoku(self, board: list[list[str]]) -> None:
        # print('\n\n\n\n\n\n\n\n\n\n\n\n\n')
        def dfs(r, c):
            # self.printBoard(board)
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
        self.printBoard(board)

    def printBoard(self, board):
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


board = [
    ["5","3",".",".","7",".",".",".","."],
    ["6",".",".","1","9","5",".",".","."],
    [".","9","8",".",".",".",".","6","."],
    ["8",".",".",".","6",".",".",".","3"],
    ["4",".",".","8",".","3",".",".","1"],
    ["7",".",".",".","2",".",".",".","6"],
    [".","6",".",".",".",".","2","8","."],
    [".",".",".","4","1","9",".",".","5"],
    [".",".",".",".","8",".",".","7","9"]
    ]
# board = [
# ["1",".",".",".","7",".","3",".","."],
# [".","8",".",".","2",".","7",".","."],
# ["3",".",".",".","8","9",".",".","4"],
# ["8","4",".",".",".","1","9",".","3"],
# [".",".","3","7",".","8","5",".","."],
# ["9",".","1","2",".",".",".","7","8"],
# ["7",".",".","3","5",".",".",".","9"],
# [".",".","9",".","4",".",".","5","."],
# [".",".","4",".","1",".",".",".","2"]
# ]

start_time = time.time()
Solution().solveSudoku(board)
print("--- %s seconds ---" % (time.time() - start_time))
